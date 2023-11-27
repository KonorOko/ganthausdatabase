import time
import streamlit as st
import pandas as pd
from sqlalchemy.sql import text
from components.header import Header
from components.footer import Footer
from manage import DataBase

    
class Add:
    def __init__(self, database):
        self.database = database
        self.query_venta = text(
            "INSERT INTO Venta (Fecha, Total, MontoPagado, ID_Cliente, ID_Empleado) VALUES (:Fecha, :Total, :MontoPagado, :ID_Cliente, :ID_Empleado);")
        self.query_empleado = text(
            "INSERT INTO Empleado (Nombre, Apellido, Telefono, Correo, Puesto) VALUES (:Nombre, :Apellido, :Telefono, :Correo, :Puesto);"
        )
        self.query_cliente = "SELECT * FROM Cliente"
        self.query_vendedor = "SELECT * FROM Empleado WHERE Puesto = 'Vendedor'"
        
    def venta(self):
        with st.form("Agregar_venta", clear_on_submit=True):
            st.write("Agrega informacion a la base de datos")
            
            # get names of clients
            df_cliente = pd.DataFrame(self.database.get_data(self.query_cliente))
            nombre_clientes = df_cliente[["Nombre", "Apellido"]].values.tolist()
            nombre_clientes = [f"{nombre} {apellido}" for nombre, apellido in nombre_clientes]

            # nombres de vendedores
            df_vendedor = pd.DataFrame(self.database.get_data(self.query_vendedor))
            nombre_vendedores = df_vendedor[["Nombre", "Apellido"]].values.tolist()
            nombre_vendedores = [f"{nombre} {apellido}" for nombre, apellido in nombre_vendedores]
            
            spacerfrom1, col1form, spacer2form, col2form, spacerform3 = st.columns([0.01 ,0.485, 0.01, 0.485, 0.01])
            with col1form:
                numero_de_factura = st.text_input("Datos de factura", placeholder= "Número de factura")
                nombre_cliente = st.selectbox("Cliente", (nombre_clientes), index=None, 
                                              placeholder="Seleccione un cliente")
                total = st.number_input("Monto Total", min_value=0, step=1, value=0)
                distribucion = st.selectbox("Distribucion", ("Directa", "Sub-distribución"), placeholder= "Tipo de distribución", index= None)
            with col2form:
                vendedor = st.selectbox("Vendedor", (nombre_vendedores), placeholder= "Nombre del vendedor", index= None)
                fecha = st.date_input("Fecha de compra", value=None, format="DD/MM/YYYY")
                pagado = st.number_input("Monto Pagado", min_value=0, step=1, value=0)
                submitted = st.form_submit_button("Modificar", use_container_width=True, 
                                                  type="secondary")
            
            if submitted:
                id_cliente = self.database.get_data("SELECT ID_Cliente From Cliente WHERE :Nombre = Nombre and :Apellido = Apellido", 
                                                params={"Nombre": nombre_cliente.split()[0], "Apellido": nombre_cliente.split()[1]})
                id_cliente = pd.DataFrame(id_cliente).iloc[0,0]
                info = {"Fecha": fecha, "Total": total, "MontoPagado": pagado, "ID_Cliente": id_cliente, "ID_Empleado": 1}
                try:
                    self.database.insert_data(self.query_venta, info)
                    st.toast("Venta agregada con éxito")
                    
                except Exception as e:
                    st.toast("No se pudo agregar la venta")

    def empleado(self):
        with st.form("Agregar_empleado", clear_on_submit= True):
            st.write("Agregar informacion a la base de datos")
            spacerfrom1, col1form, spacer2form, col2form, spacerform3 = st.columns([0.01 ,0.485, 0.01, 0.485, 0.01])
            with col1form:
                nombre_empleado = st.text_input("Nombre", placeholder="Nombre de empleado")
                telefono = st.text_input("Telefono", placeholder="Número telefónico")
                puesto = st.selectbox("Puesto", ("Gerente", "Vendedor", "Repartidor", "Administración"),
                                       placeholder="Puesto que ocupa en la empresa", index= None)

            with col2form:
                apellido_empleado = st.text_input("Apellido", placeholder="Apellido de empleado")
                correo = st.text_input("Correo", placeholder="Correo electrónico")
                submitted = st.form_submit_button("Agregar", use_container_width=True)
            
            if submitted:
                info = {"Nombre": nombre_empleado, "Apellido": apellido_empleado, 
                        "Telefono": telefono, "Correo": correo, "Puesto": puesto}
                try:
                    self.database.insert_data(self.query_empleado, info)
                    st.toast("Venta agregada con éxito")
                    
                except Exception as e:
                    st.toast("No se pudo agregar la venta")


class Delete:
    def __init__(self, database: DataBase):
        self.database = database
        self.query_venta = text(
            "DELETE FROM Venta WHERE ID_Venta = :ID_Venta;")
        self.query_empleado = text(
            "DELETE FROM Empleado Where ID_Empleado = :ID_Empleado;")
        
    def venta(self):
        with st.form("Venta"):
            st.write("Elimina un registro de la base de datos")
            spacerfrom1, col1form, spacer2form, col2form, spacerform3 = st.columns([0.01 ,0.485, 0.01, 0.485, 0.01])
            with col1form:
                numero_de_registro = st.text_input("Ingresa el ID del registro a borrar")
            with col1form:
                submitted_venta = st.form_submit_button("Eliminar")

            if submitted_venta:
                try:
                    numero_de_registro = int(numero_de_registro)
                    self.database.delete_data(self.query_venta, params={
                        "ID_Venta": numero_de_registro
                    })
                    st.toast("Se elimino el registro correctamente")
                except Exception as e:
                    st.toast("No se pudo eliminar el registro")

    def empleado(self):
        with st.form("Empleado"):
            st.write("Elimina un registro de la base de datos")
            spacerfrom1, col1form, spacer2form, col2form, spacerform3 = st.columns([0.01 ,0.485, 0.01, 0.485, 0.01])
            with col1form:
                numero_de_empleado = st.text_input("Ingresa el ID del empleado")

            with col2form:
                submitted_empleado = st.form_submit_button("Eliminar")

            if submitted_empleado:
                try:
                    numero_de_empleado = int(numero_de_empleado)
                    self.database.delete_data(self.query_empleado, params={
                        "ID_Empleado": numero_de_empleado
                    })
                except Exception as e:
                    st.toast("No se pudo eliminar el empleado")


class Modify:
    def __init__(self, database: DataBase) -> None:
        self.database = database
        self.query_cliente = "SELECT * FROM Cliente"
        self.query_vendedor = "SELECT * FROM Empleado WHERE Puesto = 'Vendedor'"

    def venta(self):
        with st.form("Venta", clear_on_submit=True):
            # get names of clients
            df_cliente = pd.DataFrame(self.database.get_data(self.query_cliente))
            nombre_clientes = df_cliente[["Nombre", "Apellido"]].values.tolist()
            nombre_clientes = [f"{nombre} {apellido}" for nombre, apellido in nombre_clientes]

            # get names of sellers
            df_vendedor = pd.DataFrame(self.database.get_data(self.query_vendedor))
            nombre_vendedores = df_vendedor[["Nombre", "Apellido"]].values.tolist()
            nombre_vendedores = [f"{nombre} {apellido}" for nombre, apellido in nombre_vendedores]

            st.write("Modifica un registro")
            
            spacerfrom1, col1form, spacer2form, col2form, spacerform3 = st.columns([0.01 ,0.485, 0.01, 0.485, 0.01])
            with col1form:
                id_venta = st.text_input("ID del registro a modificar", placeholder= "Número de registro")
                vendedor = st.selectbox("Vendedor", (nombre_vendedores),placeholder= "Nombre del vendedor", index= None)
                nombre_cliente = st.selectbox("Cliente", (nombre_clientes), index=None, 
                                              placeholder="Seleccione un cliente")
                total = st.number_input("Monto Total", min_value=0, step=1, value=0)
                distribucion = st.selectbox("Distribucion", ("Directa", "Sub-distribución"), placeholder= "Tipo de distribución", index= None)
            with col2form:
                numero_de_factura = st.text_input("Datos de factura", placeholder= "Ingrese número de factura")
                fecha = st.date_input("Fecha de compra", value=None, format="DD/MM/YYYY")
                pagado = st.number_input("Monto Pagado", min_value=0, step=1, value=0)
                submitted = st.form_submit_button("Modificar", use_container_width=True, 
                                                  type="secondary")
            
            if submitted:
                id_cliente = self.database.get_data("SELECT ID_Cliente From Cliente WHERE :Nombre = Nombre and :Apellido = Apellido", 
                                                params={"Nombre": nombre_cliente.split()[0], "Apellido": nombre_cliente.split()[1]})
                id_cliente = pd.DataFrame(id_cliente).iloc[0,0]
                info = {"Fecha": fecha, "Total": total, "MontoPagado": pagado, "ID_Cliente": id_cliente, "ID_Empleado": 1}
                try:
                    self.database.insert_data(self.query_venta, info)
                    st.toast("Venta agregada con éxito")
                    
                except Exception as e:
                    st.toast("No se pudo agregar la venta")

    def empleado(self):
        with st.form("Empleado"):
            st.write("Modifica un registro de la base de datos")
            spacerfrom1, col1form, spacer2form, col2form, spacerform3 = st.columns([0.01 ,0.485, 0.01, 0.485, 0.01])
            with col1form:
                numero_de_empleado = st.text_input("Ingresa el ID del empleado", placeholder="ID del empleado")
                apellido = st.text_input("Apellido", placeholder="Apellido del empleado")

            with col2form:
                nombre = st.text_input("Nombre", placeholder="Nombre del empleado")
                telefono = st.text_input("Telefono", placeholder="Telefono del empleado")
                submitted_empleado = st.form_submit_button("Modificar", use_container_width=True)

            if submitted_empleado:
                try:
                    numero_de_empleado = int(numero_de_empleado)
                    self.database.delete_data(self.query_empleado, params={
                        "ID_Empleado": numero_de_empleado
                    })
                except Exception as e:
                    st.toast("No se pudo modificar el empleado")


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
                eliminar = Delete(self.database)
                modificar = Modify(self.database)
                
                if option == "Agregar":
                    agregar.venta()
                        
                elif option == "Modificar":
                    modificar.venta()
                        
                elif option == "Eliminar":
                    eliminar.venta()
                    
            with col2:
                reload = st.button(":arrows_counterclockwise:", use_container_width=True)
                st.dataframe(self.database.get_data("SELECT * FROM Venta"), use_container_width=True, hide_index=True)
                if reload:
                    st.cache_data.clear()

        with tab_empleado:
            col1, spacer1, col2, spacer2 = st.columns([0.6, 0.01, 0.38, 0.01])
            with col1:
                if option == "Agregar":
                    agregar.empleado()

                elif option == "Modificar":
                    modificar.empleado()

                elif option == "Eliminar":
                    eliminar.empleado()

            with col2:
                reload2 = st.button(":arrows_counterclockwise:", use_container_width=True, key="reload2")
                st.dataframe(self.database.get_data("SELECT * FROM Empleado"), use_container_width=True, hide_index=True)
                if reload2:
                    st.cache_data.clear()


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