import pandas as pd 
import numpy as np
import matplotlib.pyplot as plt
import streamlit as st

st.set_page_config(page_title="Tracer Commodities Stock Status")
st.title("Tracer Commodities Stock Status")

upload_file = st.file_uploader("Select your Dataset")
if upload_file is not None:
    data = pd.read_excel(upload_file)
    #st.write(data)

else:
    st.stop()

def convert_df(df):
    return df.to_csv().encode("utf-8")

#data.drop(data.index[:4], inplace = True)
#data.rename(columns=data.iloc[0], inplace = True)
#data.drop([4], axis = 0, inplace = True)
data = data.loc[:, data.columns.notna()]
data.dropna(axis = 0, how = "all", inplace = True)

#Changing Data Types
data[['AMC', 'Ending Balance', 'MOS']] = data[['AMC', 'Ending Balance', 'MOS']].astype(np.int64)

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

                               
data = data[["Province Name", "District Name","Facility Name", "Product Name","MOS","AMC", "Ending Balance"]]


#Filtering out Tracer Commodities
data = data.loc[(data["Product Name"].isin(["Tenofovir/Lamivudine/Dolu300/300/50mg(30Tabs)","Tenofovir/Lamivudine/Dolu300/300/50mg (90Tabs)",
"Artemether - 4X6","Male Condoms","Control Pill","Amoxycilin 250mg disp tabs","Amoxycilin 250mg Caps","Ferrous + folic 60+0.4mg tab","Paracetamol 500mg Tabs",
"ORS+Zinc tabs","Lignocaine Hcl plain  2%","RUTF","Abacavir 120mg +Lamivudine 60mg tablets","Latex Gloves (Medium)","Surgical Face Masks","Oxytocin 10 IU/ml", "Ceftriaxone 250mg",
"Penicillin benzathine.    1.44g=2 4MU","RHZE 150/75/400/275mg tablet","Determine","Rapid Malaria Diagnostic Test (Pf)","Rapid Diagnostic Test PF/PAN"]))]

#Renaming TLD and RDT
data = data.replace({"Product Name": {"Tenofovir/Lamivudine/Dolu300/300/50mg(30Tabs)": 'TLD', "Tenofovir/Lamivudine/Dolu300/300/50mg (90Tabs)" :'TLD',
                                     "Rapid Malaria Diagnostic Test (Pf)" : "RDT", "Rapid Diagnostic Test PF/PAN" : "RDT"}})

data = data.groupby(["Province Name", "District Name","Facility Name", "Product Name"])[["Ending Balance", "AMC"]].sum().reset_index()

data = data.assign(Calculated_MOS = np.where(data["AMC"] == 0, 999, data['Ending Balance']/data["AMC"])) 

threshhold = int(len(data["Product Name"].unique())*0.8)

data1 = data.loc[data.Calculated_MOS >= 3]

#data1.groupby(["District Name","Facility Name"])["Product Name"].unique()

data2 = data1.groupby(["Province Name", "District Name","Facility Name"])["Product Name"].nunique().reset_index()

data3 = data2.loc[data2["Product Name"]>= threshhold]

data3 = data3.assign(ID = data3["District Name"]+"-"+data3["Facility Name"])

data1 = data1.assign(ID = data1["District Name"]+"-"+data1["Facility Name"])

st.title("Percentage of Facilities with 80% Tracer Commodities with MOS greater or equal to 3 months")
percentage = round(data3.ID.nunique()/data1.ID.nunique()*100,2)
st.write(percentage)


data5 = data3.groupby(["Province Name","District Name"])["Facility Name"].nunique().reset_index()
data5 = data5.assign(Total_Facilities = data["Facility Name"].nunique())
data5 = data5.assign(Percentage_of_Facilities_with_80_percent_Tracer_Commodities_per_District = round((data5["Facility Name"]/data5["Total_Facilities"])*100,2))
data5.rename(columns = {"Facility Name" : "Number of Facilities with 80% Tracer Commodities"}, inplace = True)
data55 = convert_df(data5)
st.title("Percentage of Facilities with 80% Tracer Commodities per district")
st.write(data5)
st.download_button("Download", data55, "Percentage of facilities per district.csv","txt/csv")


data4 = data1.loc[data1.ID.isin(data3.ID.values)]

data4 = data4[["Province Name","District Name"	,"Facility Name","Product Name","Ending Balance","AMC","Calculated_MOS"]]
data44 = convert_df(data4)
st.title("Facilities with 80% Tracer Commodities with MOS greater or equal to 3 months")
st.write(data4)
st.download_button("Download", data44, "Faclities_with_MOS>=3.csv","txt/csv")