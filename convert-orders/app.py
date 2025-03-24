import streamlit as st
import pandas as pd


def load_data(uploaded_file):
    return pd.read_csv(uploaded_file, delimiter=";", encoding="utf-8-sig")


def count(row):
    nb_ga4, nb_ga5, nb_ca, nb_cs, nb_o = 0, 0, 0, 0, 0
    if row["name"] == "Agenda genevois":
        if row["options"] == "Format:A4":
            nb_ga4 = row["quantity"]
        if row["options"] == "Format:A5":
            nb_ga5 = row["quantity"]

    if row["name"] == "Agenda cantons":
        nb_ca = row["quantity"]

    if row["name"].startswith("Offre genevoise"):
        nb_o = row["quantity"]
        if row["options"] == "Agenda:A4":
            nb_ga4 = row["quantity"]
            nb_cs = row["quantity"]
        if row["options"] == "Agenda:A5":
            nb_ga5 = row["quantity"]
            nb_cs = row["quantity"]

    if row["name"].startswith("Offre cantons"):
        nb_o = row["quantity"]
        nb_ca = row["quantity"]
        nb_cs = row["quantity"]

    return row["order_number"], nb_ga4, nb_ga5, nb_ca, nb_cs, nb_o, row["total"]


def convert(df):
    df = df.apply(count, axis=1, result_type="expand")
    df.columns = ["name", "GE - A4", "GE - A5", "CA", "CS", "OFFRE", "total"]


    df = (
        df.groupby("name")
        .agg(
            {
                "GE - A4": "sum",
                "GE - A5": "sum",
                "CA": "sum",
                "CS": "sum",
                "OFFRE": "sum",
                "total": "sum",
            }
        )
        .reset_index()
    )

    return df
    #  df.to_csv("converted_orders.csv", index=False)


def main():
    st.title("Convert orders from MyCommerce")
    st.write(
        """
        Upload an export with orders from MyCommerce.
        A output file will be generate with the count of
        products used in those orders.
        """
    )
    
    uploaded_file = st.file_uploader("Upload CSV File", type=["csv"])
    if uploaded_file is not None:
        try:
            records = load_data(uploaded_file)
            st.success("Excel file successfully uploaded and processed!")
            ppt_buffer = convert(records)
            ppt_buffer = convert(records)
            csv_data = ppt_buffer.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="Download Converted Orders",
                data=csv_data,
                file_name="converted_orders.csv",
                mime="text/csv",
            )
        except Exception as e:
            st.error(f"An error occurred while generating the presentation: {e}")


if __name__ == "__main__":
    main()