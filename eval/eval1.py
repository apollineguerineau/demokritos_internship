import pandas as pd
import matplotlib.pyplot as plt
from sklearn.metrics import roc_curve, roc_auc_score
import numpy as np

# labelled_data = pd.read_csv("/Users/apollineguerineau/Documents/ENSAI/3A/Greece/internship/eval/dataset_rag.csv")
# fetched_pages = pd.read_csv("/Users/apollineguerineau/Documents/ENSAI/3A/Greece/internship/eval/fetched_pages/test1.csv")

labelled_data = pd.read_csv("/Users/apollineguerineau/Documents/ENSAI/3A/Greece/internship/eval/ML_MOF_Diffusion/dataset_ML_MOF_Diffusion.csv")

labelled_data_relevants = labelled_data[labelled_data['relevance']==1]
print(f'nb relevant papers in total : {len(labelled_data_relevants)}')
fetched_pages = pd.read_csv("/Users/apollineguerineau/Documents/ENSAI/3A/Greece/internship/eval/ML_MOF_Diffusion/fetched_pages/seed-query-expansor_cos-sim2.csv")
# # labelled_data['relevance'] = labelled_data['relevance'].replace({1: 0, 2: 1})
# # labelled_data.to_csv("/Users/apollineguerineau/Documents/ENSAI/3A/Greece/internship/eval/dataset_ML_MOF_Diffusion.csv", index=False)

print(f'nb papers fetched : {len(fetched_pages)}')

merged_data = pd.merge(labelled_data, fetched_pages, on="url", how="inner")
merged_data['relevance'] = merged_data['relevance'].fillna(0)
print(f'nb papers already labelled : {len(merged_data)}')
relevants = merged_data[merged_data['relevance']==1]
print(f'nb relevant papers fetched : {len(relevants)}')

left_join = pd.merge(fetched_pages, labelled_data, on="url", how="left", indicator=True)
only_in_fetched = left_join[left_join["_merge"] == "left_only"]
only_in_fetched = only_in_fetched.drop(columns=["_merge"])
print(f'nb new papers : {len(only_in_fetched)}')
# only_in_fetched.to_csv("/Users/apollineguerineau/Documents/ENSAI/3A/Greece/internship/eval/fetched_pages/test3_not_labelled.csv")

y_true = merged_data['relevance']  # Valeurs vraies (0 ou 1)
y_scores = merged_data['score']    # Scores prédits par le modèle

# Calculer les courbes ROC et AUC
fpr, tpr, thresholds = roc_curve(y_true, y_scores)
# Rechercher l'indice où TPR est le plus proche de 0.8
target_tpr = 0.99
closest_index = np.argmin(np.abs(tpr - target_tpr))

# Récupérer le seuil correspondant
optimal_threshold = thresholds[closest_index]

roc_auc = roc_auc_score(y_true, y_scores)

# Tracer la courbe ROC
plt.figure(figsize=(10, 8))
plt.plot(fpr, tpr, label=f"ROC Curve (AUC = {roc_auc:.2f})", color='blue')
plt.plot([0, 1], [0, 1], 'r--', label="Random Guessing")  # Diagonale pour référence

# Annoter certains points avec les seuils
for i in range(0, len(thresholds), max(1, len(thresholds)//10)):  # Échantillonner 10 points environ
    plt.annotate(f"{thresholds[i]:.3f}", (fpr[i], tpr[i]), 
                 textcoords="offset points", xytext=(-10, 10), ha='center', fontsize=9, color='green')

# Labels et légende
plt.xlabel("False Positive Rate (FPR)")
plt.ylabel("True Positive Rate (TPR)")
plt.title("ROC Curve with Thresholds")
plt.legend(loc="lower right")
plt.grid(alpha=0.3)
plt.show()

classified_data = merged_data[merged_data['score']>=optimal_threshold]
classified_data_relevants = classified_data[classified_data['relevance']==1]
print(f'nb papers to keep with score {optimal_threshold}: {len(classified_data)}')
print(f'nb relevant papers kept : {len(classified_data_relevants)}')


classified_data_new_fetched = only_in_fetched[only_in_fetched['score']>=optimal_threshold]
print(f'nb of new papers to keep with score {optimal_threshold}: {len(classified_data_new_fetched)}')
classified_data_new_fetched.to_csv("/Users/apollineguerineau/Documents/ENSAI/3A/Greece/internship/eval/ML_MOF_Diffusion/fetched_pages/snew_possible_relevants.csv")
