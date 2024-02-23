from fastapi import FastAPI, Query
from fastapi.responses import JSONResponse
from google_sheets import GoogleSheetEditor
from api import DataProcessor

app = FastAPI()


@app.get("/")
async def root():
    return JSONResponse({'hello': 'world'})


@app.get("/update_member_count")
async def update_mebmer_count(url: str, number: str):
    editor = GoogleSheetEditor()
    editor.update_mambers_count(link=url, number=number)
    return {"success": True}


@app.get("/add_links")
async def add_link(links: str = Query(...), names: str = Query(...)):
    editor = GoogleSheetEditor()
    editor.add_links(links=links.split(","), names=names.split(","))
    return {"success": True}


@app.get("/spends")
async def spend():
    print(1232312837621)
    editor = GoogleSheetEditor()
    data_processor = DataProcessor()
    accounts = await data_processor.get_all_accounts()
    data = editor.get_all_sheet_data()
    rows = [[row[0], row[1], row[-3], row[-1]] if len(row) == 11 else [row[0], row[1], row[-3], ""] for row in data]
    for row in rows:
        if row[1] == "":
            print("NAME IS EMPTY")
            continue
        elif row[-1] != "":
            print("ID ALREADY EXIST")
            acc = row[-1]
            acc = accounts.get(acc)
            response = await data_processor.get_response(acc_id=acc)
            spend = await data_processor.get_spend_by_name(target_name=row[1],
                                                           response=response)
            editor.update_data("F", row[0], spend)
            continue
        else:
            print("SEARCH ACC")
            print(accounts)
            for acc in accounts:
                print(acc)
                response = await data_processor.get_response(acc_id=acc)
                spend = await data_processor.get_spend_by_name(
                    target_name=row[1], response=response)
                if spend is None:
                    continue
                editor.update_data("K", row[0], acc)
                editor.update_data("F", row[0], spend)
                break
