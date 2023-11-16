import pandas as pd 
import numpy as np
import matplotlib.pyplot as plt
import streamlit as st

st.set_page_config(page_title="Tracer Commodities Stock Status")
st.title(":blue[Tracer Commodities Stock Status]")

upload_file = st.file_uploader(":red[**Select your Dataset**]")
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

                               
data1 = data[["Province Name", "District Name","Facility Name", "Product Name","MOS","AMC", "Ending Balance"]]

data2 = data1[~data1["Facility Name"].str.startswith('CBD')]
data2 = data2[~data2["Facility Name"].str.startswith('cbd')]
data3 = data2[~data2["Facility Name"].str.startswith('GL ')]
data3 = data3[~data3["Facility Name"].str.startswith('G/L ')]

unique_fac = data3.groupby(["Province Name","District Name"])["Facility Name"].nunique().reset_index()


#Filtering out Tracer Commodities
data4 = data3.loc[(data3["Product Name"].isin(["Tenofovir/Lamivudine/Dolu300/300/50mg(30Tabs)","Tenofovir/Lamivudine/Dolu300/300/50mg (90Tabs)",
"Artemether - 4X6","Male Condoms","Control Pill","Amoxycilin 250mg disp tabs","Amoxycilin 250mg Caps","Ferrous + folic 60+0.4mg tab","Paracetamol 500mg Tabs",
"ORS+Zinc tabs","Lignocaine Hcl plain  2%","RUTF","Abacavir 120mg +Lamivudine 60mg tablets","Latex Gloves (Medium)","Surgical Face Masks","Oxytocin 10 IU/ml", "Ceftriaxone 250mg",
"Penicillin benzathine.    1.44g=2 4MU","RHZE 150/75/400/275mg tablet","Determine","Rapid Malaria Diagnostic Test (Pf)","Rapid Diagnostic Test PF/PAN"]))]


#Renaming TLD and RDT
data4 = data4.replace({"Product Name": {"Tenofovir/Lamivudine/Dolu300/300/50mg(30Tabs)": 'TLD', "Tenofovir/Lamivudine/Dolu300/300/50mg (90Tabs)" :'TLD',
                                     "Rapid Malaria Diagnostic Test (Pf)" : "RDT", "Rapid Diagnostic Test PF/PAN" : "RDT"}})



data5 =data4.groupby(["Province Name", "District Name","Facility Name", "Product Name"])[["Ending Balance", "AMC"]].sum().reset_index()

data6 = data5.assign(Calculated_MOS = np.where((data5["AMC"] == 0) & (data5['Ending Balance']>0) , 999, data5['Ending Balance']/data5["AMC"])) 

threshhold = int(len(data6["Product Name"].unique())*0.8)

data7 = data6.loc[data6.Calculated_MOS >= 3]

data8 = data7.groupby(["Province Name","District Name","Facility Name"])["Product Name"].nunique().reset_index()

data9 = data8.loc[data8["Product Name"]>= threshhold]

data10 = data9.assign(ID = data9["District Name"]+"-"+data9["Facility Name"])

data11 = data6.assign(ID = data6["District Name"]+"-"+data6["Facility Name"])

percentage = round(data10.ID.nunique()/data11.ID.nunique()*100,2)
st.subheader('Percentage of Facilities with 80% Tracer Commodities with MOS greater or equal to 3 months' )
st.title(percentage)

total_facilities = data10.ID.nunique()
st.subheader('Number of Facilities with 80% Tracer Commodities with MOS greater or equal to 3 months')
st.title(total_facilities)

data12 = data11.loc[data11.ID.isin(data10.ID.values)]

data12 = data12[["Province Name","District Name","Facility Name","Product Name","Ending Balance","AMC","Calculated_MOS"]]

data13 = data12.groupby(["Province Name","District Name"])["Facility Name"].nunique().reset_index()

merged_table = pd.merge(data13, unique_fac, on = "District Name" )
merged_table.drop(columns = "Province Name_y", inplace = True)
merged_table = merged_table.rename(columns ={"Province Name_x" : "Province Name", "Facility Name_x":"Facilities_with_80_percent", "Facility Name_y" : "Total_Facilities"})

data14 = merged_table.assign(Percentage_of_Facilities = round((merged_table["Facilities_with_80_percent"]/merged_table["Total_Facilities"])*100,2))
data55 = convert_df(data14)
st.subheader("Percentage of Facilities with 80% Tracer Commodities per District")
st.write(data14)
st.download_button("Download", data55, "Percentage of facilities per district.csv","txt/csv")

data15 = data14
data15.drop(columns = ["Province Name","Percentage_of_Facilities"], inplace = True)
data15 = data15.set_index(["District Name"])
st.title("Number of Facilities per District")
st.bar_chart(data15)

products = data12.loc[data12.Calculated_MOS >=3]
products = products.assign(ID = products["District Name"]+"-"+products["Facility Name"])
products1 = products.groupby(["Product Name"])["ID"].nunique().reset_index()
products1 = products1.rename(columns = {"ID" : "Total_Facilities"})
products1 = products1.set_index(["Product Name"])
st.title("Number of Facilities with a product")
st.bar_chart(products1)

#st.title("Percentage of Facilities with 80% Tracer Commodities per District Chart")
#data16 = data14
#data16 = data16[["District Name","Percentage_of_Facilities"]]
#data16 = data16.set_index(["District Name"])
#st.line_chart(data16)

data44 = convert_df(data12)
st.subheader("Facilities with 80% Tracer Commodities with MOS greater or equal to 3 months")
st.write(data12)
st.download_button("Download", data44, "Faclities_with_MOS>=3.csv","txt/csv")
