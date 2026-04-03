import json

nb = {
 "cells": [
  {
   "cell_type": "code",
   "execution_count": None,
   "metadata": {},
   "outputs": [],
   "source": [
    "from pyspark.sql import SparkSession\n",
    "from pyspark.sql.functions import col, to_date, desc, sum\n",
    "\n",
    "spark = SparkSession.builder.appName(\"DMartRetailAnalytics\").getOrCreate()"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": None,
   "metadata": {},
   "outputs": [],
   "source": [
    "df = spark.read.csv(\"dmart_sales(in).csv\", header=True, inferSchema=True)\n",
    "df.show(5)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": None,
   "metadata": {},
   "outputs": [],
   "source": [
    "df_cleaned = df.dropna()\n",
    "df_cleaned = df_cleaned.filter((col(\"quantity\") > 0) & (col(\"price\") > 0))\n",
    "df_cleaned = df_cleaned.withColumn(\"total_value\", col(\"quantity\") * col(\"price\"))\n",
    "df_cleaned = df_cleaned.withColumn(\"date\", to_date(col(\"timestamp\"), \"M/d/yyyy H:mm\"))\n",
    "df_cleaned.show(5)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": None,
   "metadata": {},
   "outputs": [],
   "source": [
    "sales_per_store_per_day = df_cleaned.groupBy(\"store_id\", \"date\").agg(sum(\"total_value\").alias(\"total_sales\"))\n",
    "sales_per_store_per_day.show()"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": None,
   "metadata": {},
   "outputs": [],
   "source": [
    "top_5_products = df_cleaned.groupBy(\"product_id\").agg(sum(\"total_value\").alias(\"revenue\")).orderBy(desc(\"revenue\")).limit(5)\n",
    "top_5_products.show()"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": None,
   "metadata": {},
   "outputs": [],
   "source": [
    "high_value_customers = df_cleaned.groupBy(\"customer_id\").agg(sum(\"total_value\").alias(\"total_spend\")).filter(col(\"total_spend\") > 50000)\n",
    "high_value_customers.show()"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": None,
   "metadata": {},
   "outputs": [],
   "source": [
    "df_cleaned.createOrReplaceTempView(\"sales_transactions\")"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": None,
   "metadata": {},
   "outputs": [],
   "source": [
    "spark.sql(\"\"\"\n",
    "    SELECT store_id, date, SUM(total_value) AS total_sales\n",
    "    FROM sales_transactions\n",
    "    GROUP BY store_id, date\n",
    "\"\"\").show()"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": None,
   "metadata": {},
   "outputs": [],
   "source": [
    "spark.sql(\"\"\"\n",
    "    SELECT product_id, SUM(total_value) AS revenue\n",
    "    FROM sales_transactions\n",
    "    GROUP BY product_id\n",
    "    ORDER BY revenue DESC\n",
    "    LIMIT 5\n",
    "\"\"\").show()"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": None,
   "metadata": {},
   "outputs": [],
   "source": [
    "spark.sql(\"\"\"\n",
    "    SELECT customer_id, SUM(total_value) AS total_spend\n",
    "    FROM sales_transactions\n",
    "    GROUP BY customer_id\n",
    "    HAVING SUM(total_value) > 50000\n",
    "\"\"\").show()"
   ]
  }
 ],
 "metadata": {
  "language_info": {
   "name": "python"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 5
}

with open("e:/coding/Tredence_Training/assignments/pyspark/solution.ipynb", "w") as f:
    json.dump(nb, f, indent=1)

print("done")
