import pandas as pd
import requests
import xml.etree.ElementTree as ET
import csv
import sys
import getopt

# This function downloads all clincal trials xml files into ct_xml folder

def download_XML():
    #for i in range(0,5):
    for i in range(len(df_ct)):
        print(i +1 , " out of ", len(df_ct))
        temp = df_ct.loc[i,"nct_id"]
        url_1 = 'https://clinicaltrials.gov/ct2/show/'
        url_2 = "?resultsxml=true"
        url_total = url_1 + temp + url_2
        #print(url_total)
        req = requests.get(url_total)
        with open("data/ct_xml/" + temp + ".xml" , "w" , encoding='utf-8') as file:
            print("open file : " + temp + ".xml")
            file.write(req.text)
        print("close file : " + temp + ".xml")
        #print(req)
    
def parse_XML_loc():
    ruca_df = pd.read_excel('data/RUCA/ruca_2_national.xls')

    with open("data/res_loc.csv" , "w" , newline='' , encoding="utf-8") as file:
        print("open file res_loc.csv")
        writer = csv.writer(file)
        row = ["nct_id", "start_date","completion_date" ,"phase", "condition","intervention_type","intervention_name","arm_group_type"  , "min_age" , "max_age" , "gender" ,  "healthy_vols" , "name","city" ,"state" , "zip","ruca" ,"country" ,"url" ]
        writer.writerow(row)
        #for i in range(0,1):
        for i in range(len(df_ct)):
            print(i + 1, " out of ", len(df_ct))
            temp = df_ct.loc[i,"nct_id"]
            #temp = "NCT00050960"
            url_1 = 'https://clinicaltrials.gov/ct2/show/'
            url_2 = "?resultsxml=true"
            url_total = url_1 + temp + url_2
            file_name = "data/ct_xml/" + temp + ".xml"
            tree = ET.parse(file_name)
            root = tree.getroot()
            start_date = ""
            completion_date = ""
            min_age = ""
            max_age =""
            gender = ""
            healthy_vol =""
            condition =""
            intervention_type = ""
            intervention_name = ""
            arm_group_type = ""
            phase = ""
            ruca = ""
            empty_cols = temp 
            name =""
            city =""
            state=""
            country=""
            zip =""
            location_count = 0
            try:
            #root = ET.fromstring(req.text)

                if(root.find("start_date") is not None):
                    start_date = root.find("start_date").text
                    
                
                if(root.find("completion_date") is not None):
                    completion_date = root.find("completion_date").text

                
                if(root.find("eligibility/minimum_age") is not None):            
                    min_age = root.find("eligibility/minimum_age").text
                
                
                if(root.find("eligibility/maximum_age") is not None):
                    max_age = root.find("eligibility/maximum_age").text
               
                
                if(root.find("eligibility/gender") is not None):
                    gender  = root.find("eligibility/gender").text
                
                if(root.find("eligibility/healthy_volunteers") is not None):
                    healthy_vol  = root.find("eligibility/healthy_volunteers").text
                
                if(root.find("condition") is not None):
                    condition = root.find("condition").text
                 
                if(root.find("intervention/intervention_type") is not None):
                    intervention_type = root.find("intervention/intervention_type").text
                 
                if(root.find("intervention/intervention_name") is not None):
                    intervention_name = root.find("intervention/intervention_name").text
                
                if(root.find("arm_group/arm_group_type") is not None):    
                   arm_group_type = root.find("arm_group/arm_group_type").text
                
                if(root.find("phase") is not None):
                    phase = root.find("phase").text
                

                if(root.find("location")):    
                    for elm in root.findall("location"):
                        #print(elm)
                        
                        if(elm.find("facility/name") is not None):
                            name = elm.find("facility/name").text
                            if(name == "California Cancer Care, Inc."):
                                empty_cols += ""
                       
                        
                        if(elm.find("facility/address/city") is not None):
                            city = elm.find("facility/address/city").text
                            


                        if(elm.find("facility/address/state") is not None):
                            state = elm.find("facility/address/state").text
                            
                        

                        if(elm.find("facility/address/country") is not None):
                            country = elm.find("facility/address/country").text
                            
                        

                        if(elm.find("facility/address/zip") is not None):
                            zip = elm.find("facility/address/zip").text
                            if(country == "United States"):
                                try:
                                    ruca = ruca_df.loc[ruca_df['ZIPA'] == int(zip[0:5]), 'RUCA2'].values[0]
                                except:
                                    ruca = 999
                            else:
                                ruca = 99

                        
                        row = [temp,start_date, completion_date,phase,condition,intervention_type,intervention_name,arm_group_type,min_age , max_age , gender , healthy_vol ,name,city, state,zip, ruca,country ,url_total]
                        # with open('log_errors.txt' , 'a') as file: 
                        #     file.write(empty_cols) 
                        #     file.write("\n")  
                        #     file.close()
                        
                        writer.writerow(row)
                    
                    
            except:
                min_age = ""
                max_age = ""
                gender = ""
                healthy_vol = ""
                phase = ""
                city = ""
                country = ""
                condition = ""
                intervention_name =""
                intervention_type =""
                arm_group_type = ""
                state = ""
                zip =""
                with open('log.txt' , 'a') as file:
                    file.write(temp) 
                    file.write("\n")  
                    file.close()
                    
                row = [temp,phase,condition,intervention_type,intervention_name,arm_group_type,min_age , max_age , gender , healthy_vol ,city, state, zip,country ,url_total]
                writer.writerow(row)
                writer.writerow("\n")

        print("close file")

def parse_XML():
    #ruca_df = pd.read_excel('data/RUCA/ruca_2_national.xls')

    with open("data/res.csv" , "w" , newline='' , encoding="utf-8") as file:
        print("open file res.csv")
        writer = csv.writer(file)
        row = ["nct_id", "start_date","completion_date" ,"phase", "condition","allocation","intervention_model", "primary_purpose" , "masking","intervention_type","intervention_name","arm_group_type"  , "min_age" , "max_age" , "gender" ,  "healthy_vols" ,"location_count" ,"url" ]
        writer.writerow(row)
        #for i in range(0,1):
        for i in range(len(df_ct)):
            print(i + 1, " out of ", len(df_ct))
            temp = df_ct.loc[i,"nct_id"]
            #temp = "NCT00050960"
            url_1 = 'https://clinicaltrials.gov/ct2/show/'
            url_2 = "?resultsxml=true"
            url_total = url_1 + temp + url_2
            file_name = "data/ct_xml/" + temp + ".xml"
            tree = ET.parse(file_name)
            root = tree.getroot()
            start_date = ""
            completion_date = ""
            min_age = ""
            max_age =""
            gender = ""
            healthy_vol =""
            condition =""
            intervention_type = ""
            intervention_name = ""
            arm_group_type = ""
            phase = ""
            ruca = ""
            empty_cols = temp 
            name =""
            city =""
            state=""
            country=""
            zip =""
            location_count = 0
            allocation = ""
            intervention_model = ""
            primary_purpose=""
            masking = ""
            try:
            #root = ET.fromstring(req.text)

                if(root.find("study_design_info/allocation") is not None):
                    allocation = root.find("study_design_info/allocation").text

                if(root.find("study_design_info/intervention_model") is not None):
                    intervention_model = root.find("study_design_info/intervention_model").text

                if(root.find("study_design_info/primary_purpose") is not None):
                    primary_purpose = root.find("study_design_info/primary_purpose").text
                
                if(root.find("study_design_info/masking") is not None):
                    masking = root.find("study_design_info/masking").text
                
                
                
                if(root.find("start_date") is not None):
                    start_date = root.find("start_date").text
                    
                
                if(root.find("completion_date") is not None):
                    completion_date = root.find("completion_date").text

                
                if(root.find("eligibility/minimum_age") is not None):            
                    min_age = root.find("eligibility/minimum_age").text
                
                
                if(root.find("eligibility/maximum_age") is not None):
                    max_age = root.find("eligibility/maximum_age").text
               
                
                if(root.find("eligibility/gender") is not None):
                    gender  = root.find("eligibility/gender").text
                
                if(root.find("eligibility/healthy_volunteers") is not None):
                    healthy_vol  = root.find("eligibility/healthy_volunteers").text
                
                if(root.find("condition") is not None):
                    condition = root.find("condition").text
                 
                if(root.find("intervention/intervention_type") is not None):
                    intervention_type = root.find("intervention/intervention_type").text
                 
                if(root.find("intervention/intervention_name") is not None):
                    intervention_name = root.find("intervention/intervention_name").text
                
                if(root.find("arm_group/arm_group_type") is not None):    
                   arm_group_type = root.find("arm_group/arm_group_type").text
                
                if(root.find("phase") is not None):
                    phase = root.find("phase").text
                

                if(root.find("location")):    
                    for elm in root.findall("location"):
                        #print(elm)
                        location_count += 1
       

                        
                    row = [temp,start_date, completion_date,phase,condition, allocation,intervention_model,primary_purpose,masking,  intervention_type,intervention_name,arm_group_type,min_age , max_age , gender , healthy_vol ,location_count ,url_total]
                    
                    writer.writerow(row)
                    
                    
            except:
                min_age = ""
                max_age = ""
                gender = ""
                healthy_vol = ""
                phase = ""
                city = ""
                country = ""
                condition = ""
                intervention_name =""
                intervention_type =""
                arm_group_type = ""
                state = ""
                zip =""
                with open('log.txt' , 'a') as file:
                    file.write(temp) 
                    file.write("\n")  
                    file.close()
                    
                row = [temp,phase,condition, allocation,intervention_model,primary_purpose,masking ,intervention_type,intervention_name,arm_group_type,min_age , max_age , gender , healthy_vol ,city, state, zip,country ,url_total]
                writer.writerow(row)
                writer.writerow("\n")

        print("close file")


def main():
    
    argumentList = sys.argv[1:]
    options = "d:"
    long_options = ["download" ]
    
    try:
    # Parsing argument
        arguments, values = getopt.getopt(argumentList, options, long_options)
            
        # checking each argument
        for currentArgument, currentValue in arguments:
            
            if currentArgument in ("-d", "--download"):
                print(currentArgument)
                print("fetching clinical trials info...")
                download_XML() 
    except getopt.error as err:
        # output error, and return with an error code
        print (str(err))
    #parse_XML_loc()
    parse_XML()
    #ruca = pd.read_excel("data/RUCA/ruca_2_national.xls")
    #print(ruca[ruca['ZIPA'] == 20850]['RUCA2'] )
    #print(ruca.head())

if __name__ == "__main__":
    df_ct = pd.read_csv('data/ct_attrition_dataset.csv')
    main()

