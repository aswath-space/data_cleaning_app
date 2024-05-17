from PySide6.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QComboBox, QPushButton, QTextEdit, QMessageBox
from sqlalchemy.exc import SQLAlchemyError

class SQLQueryBuilderDialog(QDialog):
    def __init__(self, parent=None, engine=None):
        super().__init__(parent)
        self.setWindowTitle('SQL Query Builder')
        self.engine = engine

        # Main layout
        main_layout = QVBoxLayout()

        # Select fields
        self.select_label = QLabel("Select Fields (comma separated):")
        self.select_input = QLineEdit()
        main_layout.addWidget(self.select_label)
        main_layout.addWidget(self.select_input)

        # From table
        self.from_label = QLabel("From Table:")
        self.from_input = QLineEdit()
        main_layout.addWidget(self.from_label)
        main_layout.addWidget(self.from_input)

        # Conditions
        self.conditions_label = QLabel("Conditions:")
        main_layout.addWidget(self.conditions_label)

        self.condition_layout = QVBoxLayout()
        self.condition_inputs = []
        self.add_condition()
        main_layout.addLayout(self.condition_layout)

        self.add_condition_button = QPushButton("Add Condition")
        self.add_condition_button.clicked.connect(self.add_condition)
        main_layout.addWidget(self.add_condition_button)

        # Execute button
        self.execute_button = QPushButton('Execute Query')
        self.execute_button.clicked.connect(self.execute_query)
        main_layout.addWidget(self.execute_button)

        # Result output
        self.result_output = QTextEdit()
        self.result_output.setReadOnly(True)
        main_layout.addWidget(self.result_output)

        self.setLayout(main_layout)

    def add_condition(self):
        """
        Add a new condition row to the query builder.
        """
        condition_layout = QHBoxLayout()

        field_input = QLineEdit()
        operator_input = QComboBox()
        operator_input.addItems(["=", ">", "<", ">=", "<=", "<>", "LIKE", "IN"])
        value_input = QLineEdit()

        remove_button = QPushButton("Remove")
        remove_button.clicked.connect(lambda: self.remove_condition(condition_layout))

        condition_layout.addWidget(field_input)
        condition_layout.addWidget(operator_input)
        condition_layout.addWidget(value_input)
        condition_layout.addWidget(remove_button)

        self.condition_inputs.append((field_input, operator_input, value_input))
        self.condition_layout.addLayout(condition_layout)

    def remove_condition(self, condition_layout):
        """
        Remove a condition row from the query builder.
        """
        for widget in condition_layout.children():
            widget.deleteLater()
        self.condition_layout.removeItem(condition_layout)
        self.condition_inputs = [ci for ci in self.condition_inputs if ci[0].parent()]

    def execute_query(self):
        """
        Build the SQL query from user inputs and execute it.
        """
        select_fields = self.select_input.text().split(',')
        from_table = self.from_input.text()
        conditions = []
        for field_input, operator_input, value_input in self.condition_inputs:
            field = field_input.text()
            operator = operator_input.currentText()
            value = value_input.text()
            conditions.append({"field": field, "operator": operator, "value": value})

        query = {
            "select": select_fields,
            "from": from_table,
            "where": conditions
        }

        sql_query = self.translate_to_sql(query)
        self.run_query(sql_query)

    def translate_to_sql(self, query):
        """
        Translate the UQL to an SQL query string.
        """
        select_clause = "SELECT " + ", ".join(query["select"])
        from_clause = "FROM " + query["from"]
        where_clause = "WHERE " + " AND ".join([f'{cond["field"]} {cond["operator"]} "{cond["value"]}"' for cond in query["where"]])
        return f"{select_clause} {from_clause} {where_clause}"

    def run_query(self, sql_query):
        """
        Execute the SQL query and display the results.
        """
        try:
            with self.engine.connect() as connection:
                result = connection.execute(sql_query)
                output = ""
                for row in result:
                    output += str(row) + "\n"
                self.result_output.setPlainText(output)
                QMessageBox.information(self, 'Success', 'Query executed successfully.')
        except SQLAlchemyError as e:
            self.result_output.setPlainText(str(e))
            QMessageBox.critical(self, 'Error', f'Failed to execute query:\n{e}')

'''
Usage Guide
- Select Fields: Enter the fields to be selected, separated by commas.
- From Table: Enter the name of the table to query from.
- Conditions: Add conditions using the Add Condition button. For each condition, specify:
   - Field: The field name to apply the condition on.
   - Operator: The comparison operator (e.g., =, >, <, LIKE).
   - Value: The value to compare against.
- Execute Query: Click the Execute Query button to build and execute the SQL query. Results will be displayed in the Result Output section.

Key Methods
- add_condition(): Adds a new row to input a condition.
- remove_condition(condition_layout): Removes a specific condition row.
- execute_query(): Gathers input data, builds the UQL, translates it to SQL, and executes the query.
- translate_to_sql(query): Converts the UQL to an SQL query string.
- run_query(sql_query): Executes the SQL query and displays the results.
'''