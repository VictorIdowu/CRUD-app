from PyQt6.QtWidgets import QMainWindow,QWidget,QApplication,QVBoxLayout,QHBoxLayout,QTableWidget,QTableWidgetItem,QLineEdit,QLabel,QPushButton,QMessageBox
import sys
import sqlite3


class MainWindow(QMainWindow):
  def __init__(self):
    super().__init__()

    self.conn = sqlite3.connect("products.db")
    self.create_table()
    self.initUI()

  def load_data(self):
    cursor = self.conn.cursor()
    cursor.execute("SELECT * FROM products")
    products = cursor.fetchall()

    self.table_widget.setRowCount(len(products))

    for row,product in enumerate(products):
      for column,value in enumerate(product):
        self.table_widget.setItem(row,column,QTableWidgetItem(str(value)))
  
  def create_table(self):
    cursor = self.conn.cursor()
    cursor.execute("""
                   CREATE TABLE IF NOT EXISTS products (
                     id INTEGER PRIMARY KEY AUTOINCREMENT,
                     name TEXT,
                     price INTEGER,
                     description TEXT
                   )
                   """)
    self.conn.commit()
  

  def initUI(self):
    self.setWindowTitle("CRUD App")
    self.setGeometry(0,0,700,500)


    central_widget = QWidget(self)
    self.setCentralWidget(central_widget)

    layout = QVBoxLayout(central_widget)

    self.table_widget = QTableWidget(self)
    
    self.table_widget.setColumnCount(4)
    layout.addWidget(self.table_widget)

    self.table_widget.setHorizontalHeaderLabels(["ID", "Name", "Price", "Description"])
    self.load_data()
    
    self.name_edit = QLineEdit()
    self.price_edit = QLineEdit()
    self.description_edit = QLineEdit()

    layout.addWidget(QLabel("Name: "))
    layout.addWidget( self.name_edit)

    layout.addWidget(QLabel("Price: "))
    layout.addWidget( self.price_edit)

    layout.addWidget(QLabel("Description: "))
    layout.addWidget( self.description_edit)

    add_button = QPushButton("Add Product", self)
    add_button.clicked.connect(self.add_product)
    
    delete_button = QPushButton("Delete Product", self)
    delete_button.clicked.connect(self.delete_product)

    update_button = QPushButton("Update Product", self)
    update_button.clicked.connect(self.update_product)

    layout.addWidget(add_button)
    layout.addWidget(delete_button)
    layout.addWidget(update_button)

  # Create
  def add_product(self):
    name = self.name_edit.text().strip()
    price = self.price_edit.text().strip()
    description = self.description_edit.text().strip()

    # adding new product to the db
    cursor = self.conn.cursor()
    cursor.execute("INSERT INTO products (name,price,description) VALUES (?,?,?)",(name,price,description))
    self.conn.commit()

    self.load_data()
    
    self.name_edit.clear()
    self.price_edit.clear()
    self.description_edit.clear()
  
  # Delete
  def delete_product(self):
    # get the selected row
    selected_row = self.table_widget.currentRow()
    if selected_row < 0 or selected_row >= self.table_widget.rowCount():
      return QMessageBox.warning(self,"Error","Please select a row")
    
    product_id = int(self.table_widget.item(selected_row,0).text())

    response = QMessageBox.question(self,"Delete Product","Do you want to delete this product?", QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)

    if response == QMessageBox.StandardButton.Yes:
      # delete the row
      cursor = self.conn.cursor()
      cursor.execute("DELETE FROM products WHERE id=?",(product_id,))
      self.conn.commit()

      self.load_data()
    else:
      return
  
  # Update
  def update_product(self):
    # get the selected row
    selected_row = self.table_widget.currentRow()

    # check if a row is selected
    if selected_row < 0 or selected_row >= self.table_widget.rowCount():
      return QMessageBox.warning(self,"Error","Please select a row")
    name = self.name_edit.text().strip()
    price = self.price_edit.text().strip()
    description = self.description_edit.text().strip()
    product_id = int(self.table_widget.item(selected_row,0).text())

    if name and price and description:
      cursor = self.conn.cursor()
      cursor.execute("UPDATE products SET name=?, price=?, description=? WHERE id=?",(name,price,description,product_id))
      self.conn.commit()

      self.load_data()
    else:
      QMessageBox.warning(self,"Error","Please fill in all fields")


app = QApplication(sys.argv)
app.setStyle("Fusion")
window = MainWindow()
window.show()
app.exec()