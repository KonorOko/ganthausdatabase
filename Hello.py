import streamlit as st
import pandas as pd
from components.header import Header
from components.footer import Footer
from manage import DataBase


class Content:
    def __init__(self, title: str, database: DataBase):
        self.title = title
        self.database = database
        self.querys = [
            "SELECT * FROM Empleado",
            "SELECT * FROM Venta"
        ]
        self.data = None
        self.database.connect()
        
    def builder(self):
        st.title(self.title)
        st.text("Aquí podrás ver los datos de la base de datos.")
        st.text(st.secrets.connections.mydb.username)
        
        option_data = st.selectbox("Seleccionar datos", ("Empleados", "Ventas"))
        if option_data == "Empleados":
            self.data = self.querys[0]
        elif option_data == "Ventas":
            self.data = self.querys[1]
        query = self.database.get_data(self.data)
        df = pd.DataFrame(query)
        
        col1, spacer1, col2, spacer2 = st.columns([0.7, 0.01, 0.28, 0.01])
        with col2:
            st.subheader("Filtros", divider=True)
            
            if option_data == "Empleados":
                opciones = st.multiselect("Filtros", df["Puesto"].unique(), label_visibility="collapsed", placeholder="Selecciona un puesto")
                if opciones:
                    filtro =df[df["Puesto"].isin(opciones)]
                    count = df.shape[0]
                else:
                    filtro = df
                    count = df.shape[0]
                
            elif option_data == "Ventas":
                opciones = st.multiselect("Filtros", df["Fecha"].unique(), label_visibility="collapsed")
                min_time = st.date_input("Mínimo", value=None, key= "min", format="DD/MM/YYYY")
                max_time = st.date_input("Máximo", value=None, key= "max", format="DD/MM/YYYY")
                
                if opciones and not min_time and not max_time:
                    filtro =df[df["Fecha"].isin(opciones)]

                elif min_time and max_time and not opciones:
                    filtro = df[(df["Fecha"] >= min_time) & (df["Fecha"] <= max_time)]

                elif opciones and min_time and max_time:
                    filtro = df[(df["Fecha"] >= min_time) & (df["Fecha"] <= max_time) & (df["Fecha"].isin(opciones))]
                    
                elif min_time and not max_time and not opciones:
                    filtro = df[(df["Fecha"] >= min_time)]
                    
                elif max_time and not min_time and not opciones:
                    filtro = df[(df["Fecha"] <= max_time)]  

                else:
                    filtro = df
                    
            bar = st.progress(0)
            count = filtro.shape[0]
            st.text(f"Total de registros: {count}")                    
        with col1:
            table = st.dataframe(filtro, use_container_width=True, hide_index=True)


def main():
    # settings
    st.set_page_config(page_title="Base de Datos", 
                       layout='wide',
                       initial_sidebar_state="collapsed")
    
    # content
    database = DataBase()
    header: Header = Header("Home")
    main_content: Content = Content("Base de Datos", database)
    footer: Footer = Footer()
    
    header.builder()
    main_content.builder()
    footer.builder()
    
    
    
if __name__ == "__main__":
    main()