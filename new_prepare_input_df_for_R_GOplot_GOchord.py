import re
import argparse
import pandas as pd

def read_gene_of_interest(gene):
    gene_list = []
    with open(gene,'r') as fr:
        for line in fr:
            gene_list.append(line.strip())
            
    print("The number of genes of interest is: ",len(gene_list))
            
    return gene_list

def read_goterm_of_interest(goterm):
    goterm_list = []
    with open(goterm,'r') as fr:
        for line in fr:
            goterm_list.append(line.strip())
            
    print("The number of goterms of interest is: ",len(goterm_list))
    
    return goterm_list

def read_goenrich_result(goenrich,term,genes):
    term2genes = {}
    df = pd.read_table(goenrich,sep="\t")
    
    if term not in df.columns:
        print("GO enrich result not contain ",term,' column')
        return "A"
        
    if genes not in df.columns:
        print("GO enrich result not contain ",genes,' column')
        return "A"
        
    else:
        for i,row in df.iterrows():
            term2genes[row[term]] = [gene.strip() for gene in re.split(";|,|:|\t|/",row[genes])]
        
        print("Total number of go enrich terms is: ",len(term2genes.keys()))
        
        return term2genes


def final_run():
    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description="prepare input data for GOchord function of GOplot package of R",
        epilog='''
        @author: MingYan
        @contact: mingyan24@126.com
        '''
    )
    
    parser.add_argument("-g",'--genes-ofinterest',required=True,help="file contain genes of interest, one per line")
    parser.add_argument("-t",'--terms-ofinterest',required=True,help="file contain terms of interest, one per line")
    parser.add_argument("-er",'--enrich-results',required=True,help='go enrich result')
    parser.add_argument("-ht",'--header-terms',required=True,help="colname of go term in enrich result")
    parser.add_argument("-hg",'--header-genes',required=True,help="colname of genes in enrich result")
    parser.add_argument("-o",'--output-files',required=True,help="specify output file name")
    
    args = parser.parse_args()
    
    geneofinterest = args.genes_ofinterest
    termofinterest = args.terms_ofinterest
    enrichresult = args.enrich_results
    headerofterms = args.header_terms
    headerofgenes = args.header_genes
    outputfile = args.output_files
    
    gene_list = read_gene_of_interest(geneofinterest)
    term_list = read_goterm_of_interest(termofinterest)
    term2genes = read_goenrich_result(enrichresult,headerofterms,headerofgenes)
    
    if term2genes == "A":
        print("Something wrong")
        
    else:
    
        final_results = {}
        new_term_list = []
    
        for term in term_list:
            if term not in term2genes.keys():
                print("The term you are interested in may not be in final go enrich result, please check carefully!")
                continue
            else:
                new_term_list.append(term)
                final_results[term] = []
        
        #print(new_term_list)
        #print(final_results)  
        
            
        for gene in gene_list:
            for term in new_term_list:
                if gene in term2genes[term]:
                    #value = 1
                    final_results[term].append(1)
                else:
                    final_results[term].append(0)
                    
        pd.DataFrame(final_results,index=gene_list).to_csv(outputfile)
        print("Congatulations!")
        print("The result was stored in ",outputfile)
        print("Next you need to read ",outputfile,' in R')
    
    
if __name__ == '__main__':
    final_run()
            