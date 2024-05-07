from PyQt6.QtWidgets import QMainWindow,QWidget,QApplication,QVBoxLayout,QHBoxLayout,QTableWidget,QTableWidgetItem,QLineEdit,QLabel,QPushButton,QMessageBox
import sys



class MainWindow(QMainWindow):
  def __init__(self):
    super().__init__()

    self.products = [
      {'name':"iPhone",'price':500,'description':"This is an iphone ytyuioojhgfdfghjklkjhgf"},
      {'name':"iPad",'price':1500,'description':"This is an ipad"},
      {'name':"iMax",'price':2500,'description':"This is an imac"},
    ]

    self.initUI()

  def initUI(self):
    self.setWindowTitle("CRUD App")
    self.setGeometry(0,0,700,500)

    central_widget = QWidget(self)
    self.setCentralWidget(central_widget)

    layout = QVBoxLayout(central_widget)

    self.table_widget = QTableWidget(self)
    self.table_widget.setRowCount(len(self.products))
    self.table_widget.setColumnCount(len(self.products[0]))
    layout.addWidget(self.table_widget)

    self.table_widget.setHorizontalHeaderLabels(self.products[0].keys())

    # Read
    for row,product in enumerate(self.products):
      for column,value in enumerate(product.values()):
        self.table_widget.setItem(row,column,QTableWidgetItem(str(value)))
    
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

    if name and price and description:
      new_product = {'name':name,'price':price,'description':description}
      self.products.append(new_product)
      
      # update the table
      row_position = len(self.products) - 1
      self.table_widget.insertRow(row_position)
      for column,value in enumerate(new_product.values()):
        self.table_widget.setItem(row_position,column,QTableWidgetItem(str(value)))
    else:
      QMessageBox.warning(self,"Error","Please fill in all fields")
    
    self.name_edit.clear()
    self.price_edit.clear()
    self.description_edit.clear()
  
  # Delete
  def delete_product(self):
    # get the selected row
    selected_row = self.table_widget.currentRow()
    if selected_row < 0 or selected_row >= self.table_widget.rowCount():
      return QMessageBox.warning(self,"Error","Please select a row")
    
    response = QMessageBox.question(self,"Delete Product","Do you want to delete this product?", QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)

    if response == QMessageBox.StandardButton.Yes:
      # delete the row
      self.table_widget.removeRow(selected_row)
      del self.products[selected_row]
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

    if name and price and description:
      updated_product = {'name':name,'price':price,'description':description}
      self.products[selected_row] = updated_product

      for column,value in enumerate(updated_product.values()):
        self.table_widget.setItem(selected_row,column,QTableWidgetItem(str(value)))
    else:
      QMessageBox.warning(self,"Error","Please fill in all fields")




app = QApplication(sys.argv)
app.setStyle("Fusion")
window = MainWindow()
window.show()
app.exec()