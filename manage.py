import streamlit as st

ssl_args = {'ssl': {'ca': '/workspaces/ganthausdatabase/cacert.pem'}}

class DataBase:
    def __init__(self):
        self.conn = None
    
    def connect(self):
        # connect to database
        try:
            self.conn = st.connection("mydb", type="sql", autocommit=False, ttl=10,
                                      connect_args=ssl_args)
            return self.conn
        except Exception as e:
            print("Connect Failed:", e)
            st.error("Failed to connect to database")
            return None

    def get_data(self, query: str, params: dict = None):
        # get data from database
        try:
            data = self.conn.query(query, params=params)
            return data
        except Exception as e:
            print(e)
            st.error("Failed to get data")
            return None
    
    def insert_data(self, query, data):
        # insert data into database
        connect_insert = self.connect()
        
        with connect_insert.session as session:
            try:
                session.execute(query, data)
                session.commit()
                return 0
            except Exception as e:
                session.rollback()
                print("Insert data failed:", e)
                st.error("Failed to insert data")
                raise
            
            finally:
                session.close()
        
    def update_data(self, data):
        # update data in database
        pass
        
    def delete_data(self, data):
        # delete data from database
        pass
        
    def close(self):
        # close database connection
        pass
    
    def reset(self):
        # reset database connection
        self.conn = None
        self.connect()
        
    