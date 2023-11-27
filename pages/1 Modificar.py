import time
import streamlit as st
import pandas as pd
from sqlalchemy.sql import text
from components.header import Header
from components.footer import Footer
from manage import DataBase

    
class Add:
    def __init__(self, conn):
        self.conn = conn
        self.query_venta = text(
            "INSERT INTO Venta (Fecha, Total, MontoPagado, ID_Cliente, ID_Empleado) VALUES (:Fecha, :Total, :MontoPagado, :ID_Cliente, :ID_Empleado);")
        self.query_cliente = "SELECT * FROM Cliente"
        
    def venta(self):
        with st.form("Agregar", clear_on_submit=True):
            st.write("Agrega informacion a la base de datos")
            
            # get names of clients
            df_cliente = pd.DataFrame(self.conn.get_data(self.query_cliente))
            nombre_clientes = df_cliente[["Nombre", "Apellido"]].values.tolist()
            nombre_clientes = [f"{nombre} {apellido}" for nombre, apellido in nombre_clientes]
            
            spacerfrom1, col1form, spacer2form, col2form, spacerform3 = st.columns([0.01 ,0.485, 0.01, 0.485, 0.01])
            with col1form:
                nombre_cliente = st.selectbox("Cliente", (nombre_clientes), index=None, 
                                              placeholder="Seleccione un cliente")
                total = st.number_input("Monto Total", min_value=0, step=1, value=0)
            with col2form:
                fecha = st.date_input("Fecha de compra", value=None, format="DD/MM/YYYY")
                pagado = st.number_input("Monto Pagado", min_value=0, step=1, value=0)
                submitted = st.form_submit_button("Modificar", use_container_width=True, 
                                                  type="secondary")
            
            if submitted:
                id_cliente = self.conn.get_data("SELECT ID_Cliente From Cliente WHERE :Nombre = Nombre and :Apellido = Apellido", 
                                                params={"Nombre": nombre_cliente.split()[0], "Apellido": nombre_cliente.split()[1]})
                id_cliente = pd.DataFrame(id_cliente).iloc[0,0]
                info = {"Fecha": fecha, "Total": total, "MontoPagado": pagado, "ID_Cliente": id_cliente, "ID_Empleado": 1}
                try:
                    self.conn.insert_data(self.query_venta, info)
                    st.toast("Venta agregada con éxito")
                    st.cache_data.clear()
                    
                except Exception as e:
                    st.toast("No se pudo agregar la venta")


class Delete:
    def __init__(self, database: DataBase):
        self.database = database
        

class Content:
    def __init__(self, title: str, database: DataBase):
        self.title = title
        self.database = database
        self.database.connect()

    def builder(self):
        st.header(self.title)
        st.text("Aquí podrás agregar datos a la base de datos.")
        option = st.radio("Selecciona la modificacion que quieras hacer", 
                 ("Agregar", "Modificar", "Eliminar"), 
                 horizontal=True, index=0)
        
        tab_venta, tab_empleado = st.tabs(["Ventas", "Empleados"])
        with tab_venta:
            col1, spacer1, col2, spacer2 = st.columns([0.6, 0.01, 0.38, 0.01])
            with col1:
                agregar = Add(self.database)
                
                if option == "Agregar":
                    agregar.venta()
                        
                if option == "Modificar":
                    pass
                        
                if option == "Eliminar":
                    with st.form("Modifica la base de datos", clear_on_submit=True):
                        st.write("Modifica la base de datos")
                        spacerfrom1, col1form, spacer2form, col2form, spacerform3 = st.columns(
                            [0.01 ,0.485, 0.01, 0.485, 0.01])
                        with col1form:
                            nombre = st.text_input("Nombre")
                            total = st.number_input("Monto Total", min_value=0.0)
                        with col2form:
                            apellido = st.text_input("Apellido")
                            pagado = st.number_input("Monto Pagado", min_value=0.0)
                        submitted = st.form_submit_button("Eliminar")
                    
            with col2:
                st.dataframe(self.database.get_data("SELECT * FROM Venta"), use_container_width=True, hide_index=True)

def main():
    # settings
    st.set_page_config(page_title="Add to DB", 
                       layout='wide', 
                       initial_sidebar_state="collapsed")
    
    # content
    header = Header("Modificar")
    database = DataBase()
    content: Content = Content("Modificar base de datos", database)
    footer: Footer = Footer()
    
    header.builder()
    content.builder()
    footer.builder()
    
if __name__ == "__main__":
    main()