import pandas as pd, numpy as np, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt, seaborn as sns
sns.set_theme(style="whitegrid"); plt.rcParams["figure.dpi"]=110
df = pd.read_csv("cleaned_sales_dataset.csv", parse_dates=["Order_Date"])
d25 = df[df.Order_Date < "2026-01-01"]
def save(n): plt.tight_layout(); plt.savefig(f"charts/{n}.png"); plt.close()

# ---- descriptive stats
num = df[["Age","Quantity","Unit_Price","Total_Sales"]]
desc = num.describe().T; desc["skew"]=num.skew(); desc["median"]=num.median()
desc.round(2).to_csv("descriptive_stats_numeric.csv")
print(desc.round(2).to_string())
for c in ["Gender","City","Category","Product","Age_Group","Order_Size","Revenue_Band"]:
    print(c, df[c].value_counts(normalize=True).mul(100).round(1).to_dict())

# ---- univariate
fig,ax=plt.subplots(2,2,figsize=(11,8))
for a,(c,t) in zip(ax.flat,[("Age","Age"),("Quantity","Quantity"),("Unit_Price","Unit price"),("Total_Sales","Total sales")]):
    sns.histplot(df[c],bins=20 if c!="Quantity" else 10,ax=a,color="#4C72B0"); a.set_title(f"Distribution of {t}")
save("01_histograms")
fig,ax=plt.subplots(1,3,figsize=(15,4.5))
for a,c in zip(ax,["Category","City","Gender"]):
    order=df[c].value_counts().index; sns.countplot(data=df,x=c,order=order,ax=a,color="#55A868"); a.set_title(f"Orders by {c}"); a.tick_params(axis="x",rotation=45)
save("02_orders_by_category_city_gender")
rev=df.groupby("Category").Total_Sales.sum().sort_values(ascending=False)/1e6
ax=rev.plot.bar(color="#C44E52",figsize=(7,4.5)); ax.set_ylabel("Revenue (millions)"); ax.set_title("Revenue by category"); plt.xticks(rotation=30); save("03_revenue_by_category")

# ---- trends
m=d25.groupby(d25.Order_Date.dt.to_period("M")).Total_Sales.sum()/1e6; m.index=m.index.strftime("%b")
ax=m.plot(marker="o",figsize=(8,4.5),color="#4C72B0"); ax.set_ylabel("Revenue (millions)"); ax.set_title("Monthly revenue, 2025"); save("04_monthly_revenue")

# ---- multivariate
sns.scatterplot(data=df,x="Unit_Price",y="Total_Sales",hue="Quantity",palette="viridis",alpha=.7); plt.title("Unit price vs total sales (colour = quantity)"); save("05_scatter_price_sales")
sns.scatterplot(data=df,x="Age",y="Total_Sales",hue="Category",alpha=.6); plt.title("Age vs total sales by category"); save("06_scatter_age_sales")
sns.heatmap(num.corr(),annot=True,fmt=".2f",cmap="coolwarm",center=0); plt.title("Correlation matrix"); save("07_correlation_heatmap")
print(num.corr().round(3))
pv=df.pivot_table(index="City",columns="Category",values="Total_Sales",aggfunc="sum")/1e6
sns.heatmap(pv,annot=True,fmt=".1f",cmap="YlGnBu"); plt.title("Revenue by city and category (millions)"); save("08_heatmap_city_category")
pv2=df.pivot_table(index="Age_Group",columns="Category",values="Total_Sales",aggfunc="sum",observed=True)/1e6
sns.heatmap(pv2,annot=True,fmt=".1f",cmap="YlOrRd"); plt.title("Revenue by age group and category (millions)"); save("09_heatmap_age_category")
sns.boxplot(data=df,x="Category",y="Total_Sales",color="#8172B2"); plt.xticks(rotation=30); plt.title("Total sales spread by category"); save("10_boxplot_category")
sns.pairplot(df[["Age","Quantity","Unit_Price","Total_Sales"]],corner=True,plot_kws={"alpha":.4,"s":12}); plt.savefig("charts/11_pairplot.png"); plt.close()
# insight numbers
print("overall rev", df.Total_Sales.sum(), "AOV", df.Total_Sales.mean(), "orders", len(df))
print("elec share", df[df.Category=="Electronics"].Total_Sales.sum()/df.Total_Sales.sum())
print("top25% revenue share by orders:", df.Total_Sales.nlargest(250).sum()/df.Total_Sales.sum())
print("customers", df.groupby(["Customer_ID","Customer_Name"]).ngroups)
print(df.groupby("Category").Total_Sales.agg(["mean","median","sum"]).round(0))
print(df.groupby("Gender").Total_Sales.agg(["sum","mean"]).round(0))
