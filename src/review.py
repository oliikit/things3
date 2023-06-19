from datetime import datetime
from itertools import cycle
from textual.app import App, ComposeResult
from textual.widgets import DataTable
import things


# get all tasks for projects, order by modified date
# can add a tag if `SKIP` is around if API support?

ROWS = [
    ("Project", "Focus", "Created Date", "Last Modified Date", "Total # of Tasks"),
]

projects = things.projects()

def fetch_tasks(project_uuid):
    items = things.get(project_uuid)
    return len(items['items'])


for proj in projects:
    proj['created_datetime'] = datetime.strptime(proj["created"], "%Y-%m-%d %H:%M:%S")
    proj['modified_datetime'] = datetime.strptime(proj["modified"], "%Y-%m-%d %H:%M:%S")
    row = (proj["title"], proj["area_title"], proj["created_datetime"], proj["modified_datetime"], fetch_tasks(proj["uuid"]))
    ROWS.append(row)

cursors = cycle(["row", "cell", "column"])

class TableApp(App):
    def compose(self) -> ComposeResult:
        yield DataTable()

    def on_mount(self) -> None:
        table = self.query_one(DataTable)
        table.cursor_type = next(cursors)
        table.zebra_stripes = True
        # table.add_columns(*ROWS[0])
        # specifying keys manually for now since add_columns doesn't add keys
        table.add_column("Project", key="proj")
        table.add_column("Focus", key="focus")
        table.add_column("Created", key="created")
        table.add_column("Mod", key="mod")
        table.add_column("Tasks", key="tasks")
        table.add_rows(ROWS[1:])
        table.sort("mod")

    def key_c(self):
        table = self.query_one(DataTable)
        table.cursor_type = next(cursors)


app = TableApp()
if __name__ == "__main__":
    app.run()
