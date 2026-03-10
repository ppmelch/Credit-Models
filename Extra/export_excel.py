from libraries  import os, pd


def export_excel_all(companies, folder="financials"):

    base_path = os.getcwd()

    export_path = os.path.join(base_path, folder)
    os.makedirs(export_path, exist_ok=True)

    print("Saving files in:", export_path)

    for ticker in companies.tickers:

        filename = os.path.join(
            export_path,
            f"{ticker}_financials.xlsx"
        )

        print("Exporting:", ticker)

        with pd.ExcelWriter(filename) as writer:

            if ticker in companies.prices.columns:
                companies.prices[[ticker]].to_excel(
                    writer,
                    sheet_name="Prices"
                )

            companies.income_statements[ticker].to_excel(
                writer,
                sheet_name="Income"
            )

            companies.balance_sheets[ticker].to_excel(
                writer,
                sheet_name="Balance"
            )

            companies.cashflows[ticker].to_excel(
                writer,
                sheet_name="Cashflow"
            )

    print("✅ Export completed")