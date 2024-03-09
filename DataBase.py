import sqlite3
import flet as ft

from flet import CrossAxisAlignment, MainAxisAlignment


def main(page: ft.Page):
    page.title = "Managment App"
    page.window_height = 780
    page.window_width = 355
    page.theme_mode = 'LIGHT'

    conn = sqlite3.connect("Test.db")
    curr = conn.cursor()

    Query = """CREATE TABLE IF NOT EXISTS Student (Name TEXT, F_Name TEXT, Class TEXT)"""
    curr.execute(Query)
    print("Table Created")
    conn.close()

    page.snack_bar = ft.SnackBar(
        content=ft.Text("Hello, world!"),
        action="Alright!",
    )  

    def snackbar():
        page.snack_bar = ft.SnackBar(ft.Text(f"This Record Is Already Exist"))
        page.snack_bar.open = True
        page.update()


    def add(name, fname, classs, Table):
     if name.value == "" or fname.value == "" or classs.value == "":
        name.border_color = 'RED'
     else:
        conn = sqlite3.connect("Test.db")
        
        curr = conn.cursor()
        data = (name.value, fname.value, classs.value)
        
        # Check for duplicates
        curr.execute(Query)
        curr.execute("SELECT * FROM Student WHERE Name = ? AND F_Name = ?", (name.value, fname.value))
        duplicate = curr.fetchone()
        
        if duplicate:
            print("Entry already exists.")
            snackbar()
        else:
            Insert = "INSERT INTO Student (Name,F_Name, Class) VALUES (?,?,?)"
            curr.execute(Insert, data)
            conn.commit()
            conn.close()
            Table.rows = []
            Show_Table(Table)
            page.update()

    def Show_Table(Table):
        conn = sqlite3.connect("Test.db")
        curr = conn.cursor()
        Show = "SELECT * FROM Student"
        curr.execute(Show)
        rows = curr.fetchall()

        Table.rows = []
        for row in rows:
            print(row)

            Table.rows.append(
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text(row[0])),
                        ft.DataCell(ft.Text(row[1])),
                        ft.DataCell(ft.Text(row[2])),
                    ],
                ),
            )
        conn.close()
        page.update()

    Table = ft.DataTable(
        columns=[
            ft.DataColumn(ft.Text("First name")),
            ft.DataColumn(ft.Text("Last name")),
            ft.DataColumn(ft.Text("Class")),
        ],
        rows=[],
    )

    Bar = ft.AppBar(
        title=ft.Text("Dashboard"),
        center_title=False,
        color='WHITE',
        bgcolor='RED',
    )

    name = ft.TextField(label="Enter Name")
    fname = ft.TextField(label="Enter Father Name")
    classs = ft.Dropdown(
        label="Select Class",
        options=[
            ft.dropdown.Option("Matric"),
            ft.dropdown.Option("FSC"),
            ft.dropdown.Option("BS"),
        ],
    )
    btn = ft.ElevatedButton("Submit", on_click=lambda _: add(name, fname, classs, Table))

    page.add(Bar, name, fname, classs, btn, Table)


ft.app(target=main)
