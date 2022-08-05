## usage
```
python new_prepare_input_df_for_R_GOplot_GOchord.py -g example_data\genes.txt -t example_data\process.txt -er exampl e_data\GO_enrich_result.tsv -ht Term -hg Genes -o output.txt
```

next we need to use R

```
df1<-read.csv("output.txt",
              header=TRUE,
              sep = ",",
              row.names = 1,
              check.names = FALSE)
df1
df2<-read.csv("example_data/geneslogfc.csv")
df2
identical(rownames(df1),df2$gene_name)

df1$logFC<-df2$logFC

#install.packages("GOplot")

library(GOplot)
library(ggplot2)

p1<-GOChord(as.matrix(df1), 
            space = 0.02, 
            gene.order = 'logFC', 
            gene.space = 0.25, 
            gene.size = 5)

ggsave(filename = "p3.pdf",
       p1,
       width = 15,height = 15)


```