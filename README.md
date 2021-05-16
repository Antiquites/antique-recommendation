# product_recommender
product recommender system SVD algorithm ,and API using flask<br>
I used datasets from [amzon product review](https://nijianmo.github.io/amazon/index.html), I've choosed __Arts, Crafts and Sewing *(meta & core5 )*__ becuase the size is small<br>

the data sets after parsing and cleaning [here!](https://drive.google.com/drive/folders/1YXt1mw1pKU6XpZCtg7S5CjsNlipne7wc?usp=sharing)<br>

## cleaning data <br>
1. delete products with more than one product_id(asin)
```sql
with meta_titles(title,counts)
as
(
SELECT title,count(DISTINCT asin) counts from meta  
GROUP by title
HAVING counts > 1
)

DELETE from meta where meta.title in (SELECT title from meta_titles)
```
2. delete users with morethan one id
```sql
with core_names (reviewerName,counts)
as
(
SELECT reviewerName,count(DISTINCT reviewerID) counts from core5
GROUP by reviewerName
HAVING counts != 1
)
DELETE from core5 where reviewerName in (SELECT reviewerName from core_names)

```
3. delete users with more than on name
```sql
with core_ids(reviewerID,counts)
as
(
SELECT reviewerID ,count(DISTINCT reviewerName) counts from core5
GROUP by reviewerID
HAVING counts != 1
)
DELETE from core5 WHERE reviewerID in (SELECT reviewerID from core_ids)
```
4. create new table **(final dataset)** from joining two tables after cleaning
```sql
CREATE TABLE arts_crafts
as
SELECT meta.asin,meta.title,core5.overall as rating,meta.brand,meta.main_cat,meta.price,meta.image,core5.reviewerID,core5.reviewerName
from meta
join core5 on meta.asin = core5.asin
```

## integrated dataset used in the model: 
1. [arts_craftss](https://drive.google.com/drive/folders/1YXt1mw1pKU6XpZCtg7S5CjsNlipne7wc?usp=sharing)<br>
2. result after building th model [arts_crafts_result](https://drive.google.com/file/d/1s_QA4002tgUaOj89HwXgdcusEsSX6AfQ/view?usp=sharing)<br>

this plot shows how the density of the dataset , as we see most products have only few rating this means sparse issue and so that I used SVD algo<br>

![image](https://user-images.githubusercontent.com/43261845/118348903-957c6980-b54d-11eb-82c9-a24e1cc93eda.png)

**snapshot of the API**<br>
![image](https://user-images.githubusercontent.com/43261845/118349238-d4132380-b54f-11eb-8fc6-de31a60ee68c.png)

