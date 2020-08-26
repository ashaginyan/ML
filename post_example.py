import requests
from lxml import etree

xml = '<enter><TimeFrame>60</TimeFrame><riskprofit>1,0573180485203945614502799242</riskprofit><PATTERN_PR_P>1,3726836853699624206297784113</PATTERN_PR_P><PATTERN_PR_T>0,555555555555556</PATTERN_PR_T><R0_P>0,0371113098844870204191553414</R0_P><R0_T>5</R0_T><R0_Way>100</R0_Way><R0_Pattern>1</R0_Pattern><R_Forecast_Pattern>9</R_Forecast_Pattern><R_Forecast_Percent>70</R_Forecast_Percent><R1_P>0,0516565398457082110149902958</R1_P><R1_T>9</R1_T><R1_Way>98</R1_Way><R1_Pattern>6</R1_Pattern><R2_Pattern>6</R2_Pattern><B0_P>-0,1230680850769305306580103958</B0_P><B0_T>20</B0_T><B0_Way>0</B0_Way><B0_Pattern>6</B0_Pattern><B_Forecast_Pattern>0</B_Forecast_Pattern><B_Forecast_Percent>100</B_Forecast_Percent><B1_Way>0</B1_Way><B1_Pattern>2</B1_Pattern><P0_P>-0,2475864502912130710710250825</P0_P><P0_T>62</P0_T><P0_Way>0</P0_Way><P0_Pattern>7</P0_Pattern><P_Forecast_Pattern>-1</P_Forecast_Pattern><P_Forecast_Percent>0</P_Forecast_Percent><P1_Way>0</P1_Way><P1_Pattern>3</P1_Pattern></enter>'
root = etree.XML(xml)
js = {}
for child in root:
    js[child.tag] = child.text


#xmlbig = requests.get('http://easytrading.pw/API/HistoryEnters/getEntersFORML.ashx').text[800:2000]
#print(xmlbig)
xml2 = '<enter><TimeFrame>60</TimeFrame><riskprofit>1,6153846153846153846153846178</riskprofit><PATTERN_PR_P>1,7125237191650853889943074004</PATTERN_PR_P><PATTERN_PR_T>1,4</PATTERN_PR_T><R0_P>0,067275164358205144571392098</R0_P><R0_T>7</R0_T><R0_Way>75</R0_Way><R0_Pattern>4</R0_Pattern><R_Forecast_Pattern>9</R_Forecast_Pattern><R_Forecast_Percent>55</R_Forecast_Percent><R1_P>0,1210109949048002145347278091</R1_P><R1_T>5</R1_T><R1_Way>0</R1_Way><R1_Pattern>9</R1_Pattern><R2_Pattern>9</R2_Pattern><B0_P>-0,1717002571616530111835416542</B0_P><B0_T>18</B0_T><B0_Way>100</B0_Way><B0_Pattern>9</B0_Pattern><B_Forecast_Pattern>2</B_Forecast_Pattern><B_Forecast_Percent>80</B_Forecast_Percent><B1_Way>100</B1_Way><B1_Pattern>1</B1_Pattern><P0_P>-0,4176783685186292685844148077</P0_P><P0_T>351</P0_T><P0_Way>0</P0_Way><P0_Pattern>8</P0_Pattern><P_Forecast_Pattern>-1</P_Forecast_Pattern><P_Forecast_Percent>0</P_Forecast_Percent><P1_Way>0</P1_Way><P1_Pattern>0</P1_Pattern><Result>1</Result></enter>'

headers = {'Content-Type': 'text/xml'}

print(requests.post("https://www.googleapis.com/upload/drive/v3/files?uploadType=resumable", data=js).text)

r = requests.post(url=f'http://127.0.0.1:5000/result/post', data=js)

print(r.text)
