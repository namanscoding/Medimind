import sys
import scrapy
import json
import os


#features=dict()
#drug_name=user_drug_name
#drug_name=str(input("Drug name : "))
#str1="https://go.drugbank.com/unearth/q?searcher=drugs&query="+drug_name
class QuotesSpider(scrapy.Spider):
    name = "drug"
    def __init__(self, *args, **kwargs):
        super(QuotesSpider, self).__init__(*args, **kwargs)
        self.start_urls = kwargs.get('start_urls').split(',')

    def parse(self, response):
        
        features=dict()
        # print(response.xpath("string(//dt[@id='generic-name']/following-sibling::dd)").get())
        #print(response.xpath(            "(//dt[@id='synonyms']/following-sibling::dd//ul//li/text())") .getall())
        features['Generic Name']  =  response.xpath("//dt[@id='generic-name']/following-sibling::dd/text()").get()
        features['Synonyms']      =  response.xpath("//dt[@id='synonyms']/following-sibling::dd//ul//li/text()") .getall()
        #features['brand_names']   =  response.xpath("//dt[@id='brand-names']/following-sibling::dd").get().split(", ")
        features['brand_names']      = response.xpath("string(//dt[@id='brand-names']/following-sibling::dd)").getall()
        features['indication']      = response.xpath("string(//dt[@id='indication']/following-sibling::dd)").getall()
        #features['indication']       = response.xpath("string(//dt[@id='indication']/following-sibling::dd)").get()
        features['chemical formula']  = response.xpath("string(//dt[@id='chemical-formula']/following-sibling::dd)").getall()
        # for key,value in features.items():
        #     print(key,' : ',value)
        #     print("#")
        #     print("#")
        #     print("#")
        dic_data={
        features['Generic Name']:{
        
        'Synonyms':features['Synonyms'],
        'brand_names':features['brand_names'],
        'indication': features['indication'],
        'chemical formula': features['chemical formula']}
        }

        #add new value if file is empty
        if os.stat('db.json').st_size==0:
            json_obj=json.dumps(dic_data,indent=4)
            with open('db.json','w') as outfile:
                outfile.write(json_obj)

        #read data from file        
        with open('db.json','r') as openfile:
            json_object=json.load(openfile)

        #add value if not present in file    
        if(features['Generic Name'] not in json_object):
            print(dic_data)  
            json_obj=json.dumps(dic_data,indent=3)
            with open('db.json','a') as outfile:
                outfile.write("\n\n"+json_obj)
        else:    
            print(json_object)
#print(features)      

 #//meta[@content="Acetaminophen"]
# dic_data={
#     'Generic Name':features['Generic Name'],
#     'Synonyms':features['Synonyms'],
#     'brand_names':features['brand_names']
# }
# json_obj=json.dumps(dic_data,indent=3)
# with open('db.json','w') as outfile:
#     outfile.write(json_obj)
# with open('db.json','r') as openfile:
#     json_object=json.load(openfile)

#print(json_object)
# 
   