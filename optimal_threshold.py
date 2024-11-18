from model.classifier.similarity_classifier import SimilarityClassifier
from model.business_object.page import Page
from model.business_object.crawl_session import CrawlSession
import pandas as pd 
import matplotlib.pyplot as plt
from sklearn.metrics import roc_curve, roc_auc_score
import numpy as np

domain = "RAG_code_generation"
# domain = "ML_MOF_Diffusion"
# type_classifier = "cos_sim"
nums = [i+1 for i in range(10)]
list_thresholds = []
for num in nums : 
    type_classifier = f"hyde/hyde{num}"
    classified_data_path = f'/Users/apollineguerineau/Documents/ENSAI/3A/Greece/internship/eval/{domain}/threshold/{type_classifier}.csv'
    classified_data = pd.read_csv(classified_data_path)
    classified_data['relevance'] = classified_data['relevance'].fillna(0)


    y_true = classified_data['relevance']  # Valeurs vraies (0 ou 1)
    y_scores = classified_data['score']    # Scores prédits par le modèle

    # Calculer les courbes ROC et AUC
    fpr, tpr, thresholds = roc_curve(y_true, y_scores)
    # Rechercher l'indice où TPR est le plus proche de target_tpr
    target_tpr = 0.99
    closest_index = np.argmin(np.abs(tpr - target_tpr))

    # Récupérer le seuil correspondant
    optimal_threshold = thresholds[closest_index]

    roc_auc = roc_auc_score(y_true, y_scores)

    # # Tracer la courbe ROC
    # plt.figure(figsize=(10, 8))
    # plt.plot(fpr, tpr, label=f"ROC Curve (AUC = {roc_auc:.2f})", color='blue')
    # plt.plot([0, 1], [0, 1], 'r--', label="Random Guessing")  # Diagonale pour référence

    # # Annoter certains points avec les seuils
    # for i in range(0, len(thresholds), max(1, len(thresholds)//10)):  # Échantillonner 10 points environ
    #     plt.annotate(f"{thresholds[i]:.3f}", (fpr[i], tpr[i]), 
    #                  textcoords="offset points", xytext=(-10, 10), ha='center', fontsize=9, color='green')

    # # Labels et légende
    # plt.xlabel("False Positive Rate (FPR)")
    # plt.ylabel("True Positive Rate (TPR)")
    # plt.title("ROC Curve with Thresholds")
    # plt.legend(loc="lower right")
    # plt.grid(alpha=0.3)
    # plt.show()


    print(f'optimal threshold for hyde {num} : {optimal_threshold}')
    list_thresholds.append(optimal_threshold)


print(np.mean(list_thresholds))