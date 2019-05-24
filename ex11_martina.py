TopHitters={"Gehrig":{"atBats":8061,"hits":2721},"Ruth":{"atBats":8399,"hits":2873},"Williams":{"atBats":7706,"hits":2654}}



print("Ruth       %.3f" %float(TopHitters["Ruth"]["hits"]/TopHitters["Ruth"]["atBats"]))
print("Williams   %.3f" %float(TopHitters["Williams"]["hits"]/TopHitters["Williams"]["atBats"]))
print("Gehrig     %.3f" %float(TopHitters["Gehrig"]["hits"]/TopHitters["Gehrig"]["atBats"]))
print("The average number of hits by the baseball players was %.1f" %float((TopHitters["Ruth"]["hits"]+TopHitters["Williams"]["hits"]+TopHitters["Gehrig"]["hits"])/3))
