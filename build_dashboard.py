import pandas as pd
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.chart import BarChart, LineChart, Reference
from openpyxl.utils import get_column_letter

df = pd.read_csv("cleaned_sales_dataset.csv", parse_dates=["Order_Date"])
cols = ["Order_ID","Order_Date","Customer_ID","Age","Gender","City","Product","Category","Quantity","Unit_Price","Total_Sales","Order_Year","Order_Month","Age_Group"]
df = df[cols]; N = len(df)+1
F="Arial"
wb = Workbook(); D = wb.active; D.title="Data"
for j,c in enumerate(cols,1):
    x=D.cell(1,j,c); x.font=Font(name=F,bold=True,color="FFFFFF"); x.fill=PatternFill("solid",fgColor="1F3864")
for i,row in enumerate(df.itertuples(index=False),2):
    for j,v in enumerate(row,1):
        c=D.cell(i,j,v.to_pydatetime() if hasattr(v,"to_pydatetime") else v); c.font=Font(name=F,size=10)
        if j==2: c.number_format="yyyy-mm-dd"
        if j in (10,11): c.number_format="#,##0.00"
for j,w in enumerate([12,12,12,6,8,11,9,12,9,12,13,11,12,10],1): D.column_dimensions[get_column_letter(j)].width=w
D.freeze_panes="A2"

S = wb.create_sheet("Dashboard",0); S.sheet_view.showGridLines=False
R = lambda col: f"Data!${col}$2:${col}${N}"
navy=PatternFill("solid",fgColor="1F3864"); mid=PatternFill("solid",fgColor="2F5597"); light=PatternFill("solid",fgColor="DDEBF7")
thin=Side(style="thin",color="BFBFBF"); box=Border(left=thin,right=thin,top=thin,bottom=thin)
S.column_dimensions["A"].width=2
for c in "BCDEFGHIJKLM": S.column_dimensions[c].width=16

S.merge_cells("B1:M1"); t=S["B1"]; t.value="ApexPlanet Sales Dashboard - Static Mock-up (Task 2)"
t.font=Font(name=F,size=18,bold=True,color="FFFFFF"); t.fill=navy; t.alignment=Alignment(vertical="center",indent=1); S.row_dimensions[1].height=34
S.merge_cells("B2:M2"); S["B2"].value="Source: cleaned Task 1 dataset (Data sheet). All figures are live formulas. Revenue in INR (assumed). Monthly view covers 2025 orders."
S["B2"].font=Font(name=F,size=9,italic=True,color="595959")

# KPI tiles: label row 4, value row 5
kp=[("B","Total Revenue",f"=SUM({R('K')})","#,##0"),
    ("C","Total Orders",f"=COUNTA({R('A')})","#,##0"),
    ("D","Avg Order Value","=B5/C5","#,##0"),
    ("E","Units Sold",f"=SUM({R('I')})","#,##0"),
    ("F","Top Category","=INDEX($B$9:$B$13,MATCH(MAX($C$9:$C$13),$C$9:$C$13,0))","@"),
    ("G","Top City","=INDEX($F$9:$F$16,MATCH(MAX($G$9:$G$16),$G$9:$G$16,0))","@")]
for col,lab,f,nf in kp:
    a=S[f"{col}4"]; a.value=lab; a.font=Font(name=F,size=10,bold=True,color="FFFFFF"); a.fill=mid; a.alignment=Alignment(horizontal="center")
    b=S[f"{col}5"]; b.value=f; b.number_format=nf; b.font=Font(name=F,size=15,bold=True,color="1F3864"); b.fill=light; b.border=box; b.alignment=Alignment(horizontal="center",vertical="center")
S.row_dimensions[5].height=32

def hdr(row,col,heads,title):
    S.cell(row-1,col,title).font=Font(name=F,bold=True,size=11,color="1F3864")
    for j,h in enumerate(heads):
        c=S.cell(row,col+j,h); c.font=Font(name=F,bold=True,color="FFFFFF",size=10); c.fill=navy; c.alignment=Alignment(horizontal="center")
def cell(r,c,v,nf="General"):
    x=S.cell(r,c,v); x.font=Font(name=F,size=10); x.number_format=nf; x.border=box; return x

cats=["Electronics","Education","Furniture","Fashion","Grocery"]
cities=["Patna","Kolkata","Bengaluru","Mumbai","Delhi","Hyderabad","Pune","Gaya"]
ages=["18-25","26-35","36-45","46-55","56-65"]
months=["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]

hdr(8,2,["Category","Revenue","% of Total"],"Revenue by Category")
for i,k in enumerate(cats):
    r=9+i; cell(r,2,k); cell(r,3,f'=SUMIFS({R("K")},{R("H")},B{r})',"#,##0"); cell(r,4,f"=C{r}/$B$5","0.0%")
hdr(8,6,["City","Revenue","Orders"],"Revenue by City (excl. Unknown)")
for i,k in enumerate(cities):
    r=9+i; cell(r,6,k); cell(r,7,f'=SUMIFS({R("K")},{R("F")},F{r})',"#,##0"); cell(r,8,f'=COUNTIFS({R("F")},F{r})',"#,##0")
hdr(8,10,["Age Group","Revenue","Avg Order"],"Revenue by Age Group")
for i,k in enumerate(ages):
    r=9+i; cell(r,10,k); cell(r,11,f'=SUMIFS({R("K")},{R("N")},J{r})',"#,##0"); cell(r,12,f'=K{r}/COUNTIFS({R("N")},J{r})',"#,##0")

hdr(19,2,["Month (2025)","Month No.","Revenue","Orders"],"Monthly Revenue Trend")
for i,k in enumerate(months):
    r=20+i; cell(r,2,k); cell(r,3,i+1)
    cell(r,4,f'=SUMIFS({R("K")},{R("L")},2025,{R("M")},C{r})',"#,##0"); cell(r,5,f'=COUNTIFS({R("L")},2025,{R("M")},C{r})',"#,##0")

# charts
def bar(title,cats_ref,vals_ref,anchor,w=15,h=7.5):
    ch=BarChart(); ch.type="col"; ch.title=title; ch.legend=None; ch.width=w; ch.height=h
    ch.add_data(vals_ref,titles_from_data=True); ch.set_categories(cats_ref); S.add_chart(ch,anchor)
bar("Revenue by Category",Reference(S,min_col=2,min_row=9,max_row=13),Reference(S,min_col=3,min_row=8,max_row=13),"G19")
ln=LineChart(); ln.title="Monthly Revenue 2025"; ln.legend=None; ln.width=15; ln.height=7.5
ln.add_data(Reference(S,min_col=4,min_row=19,max_row=31),titles_from_data=True); ln.set_categories(Reference(S,min_col=2,min_row=20,max_row=31)); S.add_chart(ln,"B34")
bar("Revenue by City",Reference(S,min_col=6,min_row=9,max_row=16),Reference(S,min_col=7,min_row=8,max_row=16),"G34")

# KPI proposal
S.cell(51,2,"Proposed KPIs to Track").font=Font(name=F,bold=True,size=11,color="1F3864")
for j,h in enumerate(["KPI","Definition","Why it matters"]):
    c=S.cell(52,[2,4,8][j],h); c.font=Font(name=F,bold=True,color="FFFFFF",size=10); c.fill=navy
for col in range(2,14): S.cell(52,col).fill=navy
rows=[("Total Revenue","Sum of Total_Sales","Headline measure of business size"),
      ("Average Order Value","Revenue / number of orders","Shows spend per order; lever for upselling"),
      ("Revenue by Category","Revenue split by product category","Electronics drives about 36% of revenue, so concentration risk"),
      ("Monthly Revenue Growth","(This month - last month) / last month","Detects seasonality, e.g. the Aug-Sep dip"),
      ("Revenue by City","Revenue split by customer city","Guides regional marketing and stock"),
      ("Revenue by Age Group","Revenue split by customer age band","Identifies the highest-value customer segment")]
for i,(a,b,c) in enumerate(rows,53):
    for col,v in zip([2,4,8],[a,b,c]): S.cell(i,col,v).font=Font(name=F,size=10,bold=(col==2))
wb.save("ApexPlanet_Task2_Dashboard_Mockup.xlsx")
