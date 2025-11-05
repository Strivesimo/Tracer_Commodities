import pandas as pd 
import numpy as np
import matplotlib.pyplot as plt
import streamlit as st
import plotly.express as px

st.set_page_config(page_title="Tracer Commodities Stock Status", layout = "wide")
st.title(":blue[Tracer Commodities Stock Status - MOS]")

upload_file = st.file_uploader(":red[**Select your Dataset - (DON'T REMOVE TOP 5 BLANK ROWS)**]")
if upload_file is not None:
    data = pd.read_excel(upload_file)
    #st.write(data)

else:
    st.stop()

def convert_df(df):
    return df.to_csv().encode("utf-8")

data.drop(data.index[:4], inplace = True)
data.rename(columns = data.iloc[0], inplace = True)
data.drop([4], axis = 0, inplace = True)
data = data.loc[:, data.columns.notna()]
data.dropna(axis = 0, how = "all", inplace = True)

#Changing Data Types
data[['AMC', 'Ending Balance', 'MOS','Ordered Units']] = data[['AMC', 'Ending Balance', 'MOS','Ordered Units']].astype(np.int64)

#Renaming Districts
data["District Name"].replace({"Umzingwane": "MZINGWANE", "Murehwa": "MUREWA", "Mt DARWIN   ": "Mt DARWIN","Mount\xa0Darwin": "Mt DARWIN",
                               "GWANDA ": "GWANDA", "Seke": "SEKE", "Chirumhanzu":"CHURUMANZU", "Gokwe\xa0North": "GOKWE NORTH","GURUVE   ": "GURUVE",
                                "MARONDERA  ": "MARONDERA","UMGUZA UNIFORMED FORCES":"UMGUZA", "Centenary": "CENTENARY",
                               "HARARE UNIFORMED FORCES":"HARARE","NORTHERN HARARE":"HARARE","HARARE  ":"HARARE","NORTHERN ":"HARARE","WESTERN":"HARARE",
                               "SOUTHERN":"HARARE","CHITUNGWIZA":"HARARE","EASTERN":"HARARE", "SOUTH WESTERN":"HARARE","WEST SOUTH WEST":"HARARE",
                               "CENTRAL SOUTH EASTERN":"HARARE", "GOKWE  SOUTH":"GOKWE SOUTH","Gokwe\xa0South":"GOKWE SOUTH", "Seke": "SEKE",
                               "Matobo": "MATOBO", "KEZI / MATOBO": "MATOBO", "Chirumhanzu":"CHURUMANZU", "Gokwe\xa0North": "GOKWE NORTH","WEDZA":"HWEDZA",
                               "Hwedza":"HWEDZA","GURUVE   ": "GURUVE", "MARONDERA  ": "MARONDERA","UMGUZA UNIFORMED FORCES":"UMGUZA", "Centenary": "CENTENARY",
                                "BULAWAYO CITY CLINICS (BCC) ":"BULAWAYO","EMAKHANDENI":"BULAWAYO","NORTHERN BULAWAYO":"BULAWAYO","BULAWAYO OTHERS":"BULAWAYO",
                               "NKULUMANE":"BULAWAYO", "MWENEZI   " :"MWENEZI",
                               "BULAWAYO CITY CLINICS (BCC)":"BULAWAYO","Chikomba":"CHIVHU","CENTENARY":"MUZARABANI","UMZINGWANE":"MZINGWANE","NORTHERN":"HARARE",
                               "NORTH WESTERN":"HARARE","BULAWAYO CITY CLINICS" : "BULAWAYO", "CENTRAL HOSPITALS":"HARARE"
                               }, inplace = True)

                               
data1 = data[["Province Name", "District Name","Facility Name", "Product Name","MOS","AMC", "Ending Balance", "Ordered Units", "Stock Delivered"]]

data2 = data1[~data1["Facility Name"].str.startswith('CBD')]
data2 = data2[~data2["Facility Name"].str.startswith('cbd')]
data3 = data2[~data2["Facility Name"].str.startswith('GL ')]
data3 = data3[~data3["Facility Name"].str.startswith('G/L ')]


#Filtering out Tracer Commodities
data4 = data3.loc[(data3["Product Name"].isin(["Tenofovir/Lamivudine/Dolu300/300/50mg(30Tabs)","Tenofovir/Lamivudine/Dolu300/300/50mg (90Tabs)",
"Artemether - 4X6","Male Condoms","Control Pill","Amoxycilin 250mg disp tabs","Amoxycilin 250mg Caps","Ferrous + folic 60+0.4mg tab","Paracetamol 500mg Tabs",
"ORS+Zinc tabs","Lignocaine Hcl plain  2%","RUTF","Abacavir 120mg +Lamivudine 60mg tablets","Latex Gloves (Medium)","Surgical Face Masks","Oxytocin 10 IU/ml", "Ceftriaxone 250mg",
"Penicillin benzathine.    1.44g=2 4MU","RHZE 150/75/400/275mg tablet","Determine","Rapid Malaria Diagnostic Test (Pf)","Rapid Diagnostic Test PF/PAN",
"1st Response Malaria Combo", "Gloves","Artemether - 1X6", "Artemether - 2X6","Artemether - 3X6", "Lidocaine inj. 2%","Paracetamol 500mg tab","Paracetamol 500mg tabss",
"Latex Gloves (Large)","Gloves Nitrile","Gloves latex examin.disp. Medium","Gloves latex examin.disp. Large"]))]

#Renaming TLD, RDT, ALs and Gloves
data4 = data4.replace({"Product Name": {"Tenofovir/Lamivudine/Dolu300/300/50mg(30Tabs)": 'TLD', "Tenofovir/Lamivudine/Dolu300/300/50mg (90Tabs)" :'TLD',"Rapid Malaria Diagnostic Test (Pf)" : "RDT",
                                     "Rapid Diagnostic Test PF/PAN" : "RDT","1st Response Malaria Combo": "RDT","Latex Gloves (Medium)" : "Gloves","Gloves" : "Gloves", "Artemether - 1X6" : "ALs", 
                                     "Artemether - 2X6" : "ALs","Artemether - 3X6" : "ALs","Artemether - 4X6" : "ALs", "Lidocaine inj. 2%" : "Lidocaine inj. 2%","Lignocaine Hcl plain  2%" : "Lidocaine inj. 2%",
                                     "Latex Gloves (Large)": "Gloves","Gloves Nitrile": "Gloves","Gloves latex examin.disp. Medium": "Gloves","Gloves latex examin.disp. Large": "Gloves",
                                     "Paracetamol 500mg tab" :"Paracetamol 500mg","Paracetamol 500mg tabss" :"Paracetamol 500mg", "Paracetamol 500mg Tabs":"Paracetamol 500mg"}})



data5 =data4.groupby(["Province Name", "District Name","Facility Name", "Product Name"])[["Ending Balance", "AMC", "Ordered Units","Stock Delivered"]].sum().reset_index()

data6 = data5.assign(Calculated_MOS = np.where(((data5["AMC"] == 0) & (data5['Ending Balance']>0)) | ((data5["AMC"] == 0) & (data5['Ending Balance']==0)) , 999, data5['Ending Balance']/data5["AMC"])) 
data6 = data6.assign(Order_Fill_Rate=np.where(((data6["Stock Delivered"]==0) & (data6["Ordered Units"]== 0)) | ((data6["Stock Delivered"]>0) & (data6["Ordered Units"]== 0)),999, data6["Stock Delivered"]/data6["Ordered Units"]))
data6 = data6.assign(ID = data6["District Name"]+"-"+data6["Facility Name"])

dataa1 =data6.groupby(["Province Name", "District Name","Facility Name"])["Product Name"].size()*0.8

data7 = data6.loc[data6.Calculated_MOS >= 3]

dataa2 =data7.groupby(["Province Name", "District Name","Facility Name"])["Product Name"].size()

dataa3 = dataa2.reindex(dataa1.index, fill_value = 0)

dataa4 = dataa1.loc[dataa3 >= dataa1]

dataa5 =data6.set_index(["Province Name", "District Name","Facility Name"])

dataa6 = dataa5.loc[dataa4.index].reset_index()

products = dataa6.loc[dataa6.Calculated_MOS >=3]
products1 = products.groupby(["Product Name"])["ID"].nunique().reset_index()
products1 = products1.rename(columns = {"ID" : "Total_Facilities"})

denominator_facilities = data6.groupby(["Province Name","District Name"])["Facility Name"].nunique().reset_index()

numerator_facilities = dataa6.groupby(["Province Name","District Name"])["Facility Name"].nunique().reset_index()

percentage = round(dataa6.ID.nunique()/data6.ID.nunique()*100,2)
st.subheader(':red[Percentage of Facilities with 80% Tracer Commodities with MOS greater or equal to 3 months]' )
st.title(f"{percentage} %")

total_facilities = dataa6.ID.nunique()
st.subheader(':blue[Number of Facilities with 80% Tracer Commodities with MOS greater or equal to 3 months]')
st.title(total_facilities)

merged_table = pd.merge(numerator_facilities, denominator_facilities, on = "District Name" )
merged_table.drop(columns = "Province Name_y", inplace = True)
merged_table = merged_table.rename(columns ={"Province Name_x" : "Province Name", "Facility Name_x":"Facilities_with_80_percent", "Facility Name_y" : "Total_Reported_Facilities"})

dataa7 = merged_table.assign(Percentage_of_Facilities = round((merged_table["Facilities_with_80_percent"]/merged_table["Total_Reported_Facilities"])*100,2))
data55 = convert_df(dataa7)
st.subheader(":green[Percentage of Facilities with 80% Tracer Commodities per District - MOS]")
st.write(dataa7)
st.download_button("Download", data55, "Percentage of facilities per district - MOS.csv","txt/csv")

dataa8 = dataa7
dataa8.drop(columns = ["Province Name","Facilities_with_80_percent","Total_Reported_Facilities"], inplace = True)
dataa8 = dataa8.set_index(["District Name"])
st.subheader("Percentage of Facilities with 80% tracer commodities with 3 or more MOS per District")
st.line_chart(dataa8)

dataa6.drop(columns = "ID", inplace = True)
dataa9 = convert_df(dataa6)
st.subheader(":red[Facilities with 80% Tracer Commodities with MOS greater or equal to 3 months]")
st.write(dataa6)
st.download_button("Download", dataa9, "Faclities_with_MOS>=3.csv","txt/csv")

#OFR
st.title(":blue[Tracer Commodities Stock Status - OFR]")
data77 = data6.loc[data6.Order_Fill_Rate >= 0.6]

data88 = data77.groupby(["Province Name","District Name","Facility Name"])["Product Name"].nunique().reset_index()

data99 = data88.loc[data88["Product Name"]>= 16]

data100 = data99.assign(ID = data99["District Name"]+"-"+data99["Facility Name"])

data122 = data6.loc[data6.ID.isin(data100.ID.values)]
data122.drop(columns = "ID", inplace = True)

percentage_ofr = round(data100.ID.nunique()/data6.ID.nunique()*100,2)
st.subheader(':red[Percentage of Facilities with at least 16/20 (80%) Tracer Commodities with OFR greater or equal to 60%]' )
st.title(f"{percentage_ofr} %")

total_facilities_ofr = data100.ID.nunique()
st.subheader(':blue[Number of Facilities with at least 16/20 (80%) Tracer Commodities with OFR greater or equal to 60%]')
st.title(total_facilities_ofr)

data133 = data122.groupby(["Province Name","District Name"])["Facility Name"].nunique().reset_index()

facilities_80_percent_ofr = data3.groupby(["Province Name","District Name"])["Facility Name"].nunique().reset_index()

merged_table_ofr = pd.merge(data133, facilities_80_percent_ofr, on = "District Name" )
merged_table_ofr.drop(columns = "Province Name_y", inplace = True)
merged_table_ofr =merged_table_ofr.rename(columns ={"Province Name_x" : "Province Name", "Facility Name_x":"Facilities_with_60_percent_OFR", "Facility Name_y" : "Total_Facilities"})

data144 = merged_table_ofr.assign(Percentage_of_Facilities = round((merged_table_ofr["Facilities_with_60_percent_OFR"]/merged_table_ofr["Total_Facilities"])*100,2))
data555 = convert_df(data144)
st.subheader(":green[Percentage of Facilities with 80% Tracer Commodities per District - OFR]")
st.write(data144)
st.download_button("Download", data555, "Percentage of Facilities per District - OFR.csv","txt/csv")

dataa88 = data144
dataa88.drop(columns = ["Province Name","Facilities_with_60_percent_OFR","Total_Facilities"], inplace = True)
dataa88 = dataa88.set_index(["District Name"])
st.subheader("Percentage of Facilities with 80% Tracer Commodities with OFR greater or equal to 60%")
st.line_chart(dataa88)

dataa122 = convert_df(data122)
st.subheader(":red[Facilities with 80% Tracer Commodities with OFR greater or equal to 60%]")
st.write(data122)
st.download_button("Download", dataa122, "Faclities_with_OFR>=0.60.csv","txt/csv")


