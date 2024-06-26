import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import pickle
import numpy as np
import plotly.graph_objects as go
import plotly.figure_factory as ff
from custom_functions import plot_auc, plot_f1_score, plot_loss_curve , plot_precision_curve
from custom_functions import plot_CM_ConvnextBase, plot_CM_ConvnextTiny, plot_CM_DenseNet201, plot_CM_DenseNetFT, plot_CM_EfficientNet_B4, plot_CM_ENetB4, plot_CM_ResNet121, plot_CM_ResNetFT, plot_CM_ResNetV2,plot_CM_VGG16,plot_CM_VGG16_FT,plot_CM_VGG19

with open("models\history_DenseNet201.pkl", "rb") as file1:
    history_densenet = pickle.load(file1)
with open("models\history_VGG16.pkl", "rb") as file2:
    history_vgg = pickle.load(file2)

def show_fine_tuning():
    # Style des onglets
    st.markdown("""
        <style>
            .stTabs [data-baseweb="tab-list"] {
                display: flex;
                gap: 10px;
            }

            .stTabs [data-baseweb="tab"] {
                padding: 10px 15px;
                border: 1px solid transparent;
                border-radius: 5px 5px 0 0;
                background-color: transparent;
                cursor: pointer;
                transition: all 0.3s ease;
            }

            .stTabs [data-baseweb="tab"]:hover {
                background-color: #8f8d9b;
            }

            .stTabs [aria-selected="true"] {
                background-color:  #57546a;
                border-color: #ccc;
                border-bottom-color: transparent;
            }
        </style>""", unsafe_allow_html = True)

    tab0, tab1, tab2, tab3, tab4, tab5 = st.tabs(["📚 Rappels Deep Learning", "🛠️ Preprocessing", "📈 Modélisation", "🧰 Suivi des métriques", "💻 Modèles testés", "🤖 Modèles finaux"])
        
    #---------------------------------------------------------------------
    # Les deux fonctions suivantes pour centrer les images dans les pages
    # fonction qui coverti une image en foramt bytes
    def img_to_bytes(img_path):
        import base64
        from pathlib import Path
        img_bytes = Path(img_path).read_bytes()
        encoded = base64.b64encode(img_bytes).decode()
        return encoded
    # fonction qui coverti l'image encoder en html
    def img_to_html(img_path):
        img_html = "<img src='data:image/png;base64,{}' class='img-fluid'>".format(img_to_bytes(img_path)
        )
        return img_html
    #---------------------------------------------------------------------   
 

    ### Onglet 0 : Présentation d'un CNN
    with tab0:
        st.header("Deep Learning & CNN")
        st.write("#### 1. Réseaux de neurones artificiels")
        st.markdown('''
            Un réseau de neurones est un ensemble de couches constitués de **Perceptrons**. Ce entité de base cherche à **imiter le fonctionnement d'un neurones biologique** grâce à des concepts mathématiques notamment le produits scalaires.\n
            Un Perceptron effectue des calculs pour détecter des caractéristiques ou des tendances dans les données d’entrée.\n
            Un réseau neuronal *'**Feed-Forward**'* est constitué de plusieurs perceptron à couches multiples.
        ''')
        
        #st.image(r".\images\neurone-biologique-et-artificiel.png", caption='Un neurone biologique vs un Perceptron (neurone artificiel)')
        # chemin du fichier de l'image
        image_path = r".\images\ann_bnn_no_bg.png"
        # afficher l'image centrée avec markdown
        st.markdown("<p style='text-align: center; color: grey;'>" + img_to_html(image_path) + "</p>", unsafe_allow_html=True)
        # La légende de l'image
        st.markdown("<div style='text-align: center; color: grey;'>Un neurone biologique vs un Perceptron (neurone artificiel)</div>", unsafe_allow_html=True)
        
        # Séparateur ligne
        st.header("", divider = "gray")
        
        st.write("#### 2. Convolutional Neural Network (CNN)")
        
        st.markdown('''
        Les réseaux de neurones convolutifs désignent une sous-catégorie de réseaux de neurones : ils présentent donc toutes les mêmes caractéristiques d'un réseau de neurones. Cependant, les CNN sont spécialement conçus pour traiter des images en entrée.\n
        Leur architecture est alors plus spécifique : elle est composée de deux blocs principaux: un extracteur de caractéristiques ou partie convolutive *'**features extraction bloc**'*, et un bloc pour la classification.\n
        
        La partie convolutive est constitué des couches suivantes:
        
        - Convolution : en utilisant des **filtres** et le **produit de convolution**, les caractéristiques de l'image d'entrée sont extraites.
        - Pooling : méthode de sous échantillonnage, l'objectif est de sous-échantillonner l'entrée en réduisant sa dimension. L'intérêt est la réduction du coût de calcul **en réduisant le nombre de paramètres à apprendre**. les deux méthodes les plus utilisées sont: le **Max-Pooling** (valeur maximum) et l'**Average Pooling** (valeur moyenne).
        
        ''')
        
        #st.image(r".\images\layers_CNN.png", caption="Architecture d'un réseau de neurones convolutifs CNN")
        image_path = r".\images\layers_cnn_no_bg.png"
        # afficher l'image centrée avec markdown
        st.markdown("<p style='text-align: center; color: grey;'>" + img_to_html(image_path) + "</p>", unsafe_allow_html=True)
        # La légende de l'image
        st.markdown("<div style='text-align: center; color: grey;'>Architecture d'un réseau de neurones convolutifs CNN</div>", unsafe_allow_html=True)
        
        # Démonstration avec l'application de reconnaissance de chiffres 
        st.write("##### Démonstration en direct : fonctionnement d'un CNN")
        st.link_button("DEMO Chiffre écrit à la main", "https://adamharley.com/nn_vis/cnn/3d.html")
        
        # Intégration de la page html de démonstation CNN dans la page streamlit
        components.iframe("https://adamharley.com/nn_vis/cnn/3d.html", height=700)


    ### Premier onglet
    with tab1:
        st.header("Preprocessing des images")
        
        st.write("#### 1. Metadata des images")
        st.markdown('''
            Une étape très importante de notre projet est l'attention portée au traitement des images d'entrée. Nous avons pu voir précédemment que les images possèdent pour certaines, des dimensions et/ou un nombre de canaux différents. Il est important d'homogénéiser l'ensemble des paramètres de nos images pour assurer une bonne performance de nos modèles, et surtout, des résultats comparables. Les éléments en question sont :
            - Une dimension homogène et carrée, par défaut 299x299 pixels.
            - Un nombre de trois canaux de couleur.
            - Une normalisation de la valeur des pixels.\n
            Une fonction `preproc_img()` est conçue pour simplifier ces étapes, améliorer la reproductibilité et faciliter les ajustements. Elle retourne automatiquement les **ensembles d'entraînement et de test**.
        ''')
        
        # Séparateur ligne
        st.header("", divider = "gray")
        
        st.write("#### 2. Fonctions de pre-processing")
        # Style CSS pour listes à puces internes
        st.markdown('''
        <style>
        [data-testid="stMarkdownContainer"] ul{
            list-style-position: inside;
        }
        </style>
        ''', unsafe_allow_html = True)

        # Définir le code comme une chaîne de caractères longue
        code = """
                def preproc_img(df_images, df_masks, n_img, normalize, files_path, resolution, with_masks):
                    np.random.seed(42)
                    # Gestion des erreurs
                    if resolution[2] != 1 and resolution[2] != 3:
                        return print("Le nombre de canaux doit être de 1 (en nuances de gris) ou de 3 (en couleur)")

                    if resolution[0] != resolution[1]:
                        return print("La largeur de l'image doit être la même que sa hauteur.")
                    
                    if normalize != 'imagenet' and normalize != 'simple':
                        print(Attention : aucune normalisation n'a été appliquée. Utilisez 'imagenet' pour une normalisation standardisée selon le mode opératoire du set ImageNet ou 'simple' pour simplement normaliser la valeur des canaux entre 0 et 1.")

                    df_images_selected_list = []
                    for label, group in df_images.groupby('LABEL'):
                        n_samples = min(len(group), n_img)
                        df_images_selected_list.append(group.sample(n=n_samples, replace=False))
                    df_images_selected = pd.concat(df_images_selected_list)

                    images = []  # Initialiser une liste pour stocker les images prétraitées
                    df_masks_selected = df_masks[df_masks['FILE_NAME'].isin(df_images_selected['FILE_NAME'])] if with_masks else None

                    for i in range(len(df_images_selected)):
                        img_path = df_images_selected[files_path].iloc[i]
                        mask_path = df_masks_selected[files_path].iloc[i] if with_masks else None

                        img = Image.open(img_path)  # Charger l'image avec PIL
                        img = img.convert("L") if resolution[2] == 1 else img.convert("RGB")

                        img_resized = img.resize((resolution[0], resolution[1]))

                        # Normalisation des valeurs des pixels
                        if normalize == 'imagenet':
                            img_normalized = np.array(img_resized) / 255.0
                            img_normalized -= np.array([0.485, 0.456, 0.406]) if resolution[2] == 3 else np.mean([0.485, 0.456, 0.406])
                            img_normalized /= np.array([0.229, 0.224, 0.225]) if resolution[2] == 3 else np.mean([0.229, 0.224, 0.225])
                        elif normalize == 'simple':
                            img_normalized = img_resized / 255
                        else:
                            img_normalized = img_resized

                        images.append(img_normalized)

                    data = np.array(images).reshape(-1, resolution[0], resolution[1], resolution[2])
                    target = df_images_selected['LABEL']
                    return data, target
                """

        with st.expander("Voir le code de la fonction preproc_img()"):
            st.code(code, language = 'python')
        
        
        st.markdown('''Le processus de prétraitement des données consiste à uniformiser les données en les important via `OpenCV` avec `cv2.IMREAD_GRAYSCALE` et en les convertissant en uint8 pour économiser de la mémoire. 
                       Les images peuvent être redimensionnées à la résolution de notre choix, stockées sous forme d'arrays numpy. 
                       Une normalisation de l'intensité des pixels peut être appliquée selon les besoins et les attentes des modèles, et des méthodes d'équilibrage des classes comme l'undersampling ou l'oversampling peuvent être envisagées en raison de différences significatives dans leur répartition. 
                       Les premiers masques sont utilisés pour limiter la surface aux informations utiles, avec la possibilité de créer de nouveaux masques.
                    ''')
        
        # Séparateur ligne
        st.header("", divider = "gray")
        
        st.write("#### 3. Encodage des labels")
        
        st.markdown(''' Dernière étape après nos images propres et normalisées, il est nécessaire de transformer nos labels multiclasses en entiers afin d'assurer la compatibilité avec une les modèles de classificiation.
                        Cette étape nécessite seulement un traitement par **One Hot Encoding** grâce à `LabelEncoder()`.
                    ''')
        
        data = {
            'Classes': ['COVID', 'Lung_Opacity', 'Normal', 'Viral Pneumonia'],
            'Numéros correspondants': [0, 1, 2, 3]
        }
        df = pd.DataFrame(data)

        # Convertir le dataframe en HTML avec les styles CSS
        html_table = df.to_html(index=False, justify='center', classes='styled-table')

        # Afficher le HTML dans Streamlit avec la largeur calculée
        st.markdown(f"<div style='border: 1px solid white; border-radius: 5px; padding: 10px; background-color: #343434; line-height: 1; width: 350px; margin: 0 auto;'>{html_table}</div>", unsafe_allow_html=True)
    
    
    
    ### Deuxième onglet
    with tab2:
        st.header("Démarche de modélisation")
        st.markdown("Nous nous sommes mis d'accord pour commencer par un modèle basique, en l'occurrence **LeNet5**, eafin de prendre en main la modélisation en Deep Learning. Ensuite, travailler avec des modèles plus complexes qui sont disponibles dans **Keras Applications**, nous avons fait du **transfert learning** à partir de ces modèles-là, en réentrainant les dernières couches sur notre base de données. Enfin, avec le module **Keras Tuner** nous avons pu ajuster plus finement nos modèles.  ")
        
        # LeNet5 
        st.write("#### 1. LeNet5")
        st.markdown(''' LeNet est une structure de réseau neuronal convolutif proposée par LeCun et al. en 1998. En général, LeNet fait référence à LeNet-5 et est un réseau neuronal convolutif simple. Les réseaux neuronaux convolutifs sont une sorte de réseau neuronal feed-forward dont les neurones artificiels peuvent répondre à une partie des cellules environnantes dans la zone de couverture et donnent de bons résultats dans le traitement d'images à grande échelle. *Source: https://en.wikipedia.org/wiki/LeNet*. 
                    ''')        
        #st.image(r".\images\LeNet5_architecture.png", caption="Architecture du LeNet5")
        # chemin du fichier de l'image
        image_path = r".\images\LeNet5_architecture_no_bg.png"
        # afficher l'image centrée avec markdown
        st.markdown("<p style='text-align: center; color: grey;'>" + img_to_html(image_path) + "</p>", unsafe_allow_html=True)
        # La légende de l'image
        st.markdown("<div style='text-align: center; color: grey;'>Architecture du LeNet5</div>", unsafe_allow_html=True)
        
        st.write("##### Etudes paramétriques: nombre d'images et nombre d'Epochs")
        
        st.markdown(''' L'efficacité et la simplicité, du modèle LeNet5, nous ont permis de réaliser des études paramétriques assez rapidement afin de le nombre d'images et d'époques à partir desquels les performances du modèle n'évoluent plus. Ceci nous a permis d'économiser en temps et coût de calcul par la suite en utilisant des modèles plus complexes.  
                    ''') 
        
        col1, col2 = st.columns([1, 1])
        
        df = pd.read_csv(r"data\Lenet_nb_image.csv")
        df2 = pd.read_csv(r"data\Lenet_nb_epoque.csv") 


        col1, col2 = st.columns(2)

        with col1 :

            fig = go.Figure()

            fig.add_trace(go.Scatter(x=df['nombre_images'], y=df['Precision max'], mode='lines+markers', name='Precision max', line=dict(color='lightblue')))
            fig.add_trace(go.Scatter(x=df['nombre_images'], y=df['Precision max validation'], mode='lines+markers', name='Precision max validation', line=dict(color='salmon')))

            fig.add_vline(x=1325, line=dict(color='red', width=1, dash='dash'))
            fig.update_layout(title="Courbe d’apprentissage du modèle LeNet-5 en fonction du nombre d’images utilisées",
                            xaxis_title='Nombre d\'images',
                            yaxis_title='Précision max',
                            template='plotly_white',
                            paper_bgcolor='rgba(0,0,0,0)',
                            plot_bgcolor='rgba(0,0,0,0)',
                            legend=dict(font=dict(color='white')),
                            xaxis=dict(tickfont=dict(color='white')),
                            yaxis=dict(tickfont=dict(color='white')),
                            title_font=dict(color='white'))
            st.plotly_chart(fig)

        with col2: 

            fig2 = go.Figure()

            fig2.add_trace(go.Scatter(x=df2['Nombre epoque'], y=df2['Precision max'], mode='lines+markers', name='Precision max', line=dict(color='lightblue')))
            fig2.add_trace(go.Scatter(x=df2['Nombre epoque'], y=df2['Precision max validation'], mode='lines+markers', name='Precision max validation', line=dict(color='salmon')))

            fig2.update_layout(title="Courbe d’apprentissage du modèle LeNet-5 en fonction du nombre d’époques",
                            xaxis_title='Nombre d\'époque',
                            yaxis_title='Précision max',
                            template='plotly_white',
                            paper_bgcolor='rgba(0,0,0,0)',
                            plot_bgcolor='rgba(0,0,0,0)',
                            legend=dict(font=dict(color='white')),
                            xaxis=dict(tickfont=dict(color='white')),
                            yaxis=dict(tickfont=dict(color='white')),
                            title_font=dict(color='white'))

            st.plotly_chart(fig2)
         
               
        st.markdown('''
        Par la suite, nous entrainons les modèles avec les paramètres suivants : 
        - 900 images par classe.
        - 20 epochs.
        
        ''')
    
        # Séparateur ligne
        st.header("", divider = "gray")
              
        # 2. Keras Tuner
        st.write("#### 2. Keras Tuner")  
        st.markdown('''
        Keras Tuner est un module qui permet de réaliser une étude d’optimisation des hyperparamètres afin de trouver les meilleures combinaisons de paramètres, permettant d’ajuster un peu plus finement le modèle (O’Malley et al., 2019).\n

        Il existe plusieurs fonctions intéressantes pour la recherche de paramètres optimaux pour un ajustement plus fin des modèles. RandomSearch() est très pratique pour chercher de manière aléatoire ces hyperparamètres optimaux,  elle prend en argument le modèle, la métrique à maximiser, les paramètres à faire varier, etc.
        
        ''')

        # Définir le code comme une chaîne de caractères longue
        code = """
            # 1. Définir une fonction qui construit le modèle avec les HP
            def build_model(hp):
                model = keras.Sequential()
                model.add(layers.Flatten())
                # Tune the number of layers.
                for i in range(hp.Int("num_layers", 1, 3)):
                    model.add(
                        layers.Dense(
                            # Tune number of units separately.
                            units=hp.Int(f"units_{i}", min_value=32, max_value=512, step=32),
                            activation=hp.Choice("activation", ["relu", "tanh"]),
                        )
                    )
                if hp.Boolean("dropout"):
                    model.add(layers.Dropout(rate=0.25))
                model.add(layers.Dense(10, activation="softmax"))
                learning_rate = hp.Float("lr", min_value=1e-4, max_value=1e-2, sampling="log")
                model.compile(
                    optimizer=keras.optimizers.Adam(learning_rate=learning_rate),
                    loss="categorical_crossentropy",
                    metrics=["accuracy"],
                )
                return model

            build_model(keras_tuner.HyperParameters())
            
            
            # 2. RandomSearch pour chercher les meilleurs combinaison d'hyperparamètres
            tuner = keras_tuner.RandomSearch(
                hypermodel=build_model,
                objective="val_accuracy",
                max_trials=3,
                executions_per_trial=2,
                overwrite=True,
                directory="my_dir",
                project_name="helloworld",
            )
            """
        with st.expander("Voir le code de KerasTuner"):
            st.code(code, language = 'python')
    
        # séparer les sections avec une ligne
        st.header("", divider = "gray")
        
        # 3. Transfer Learning
        st.write("#### 3. Transfer Learning")  
        st.markdown('''
        Le transfer learning est une technique en apprentissage automatique où un modèle pré-entraîné sur une tâche est réutilisé comme point de départ pour résoudre une autre tâche similaire. 
        Plutôt que de construire un nouveau modèle à partir de zéro, on exploite les connaissances et les représentations déjà apprises (les poids), ce qui permet d'améliorer l'apprentissage sur des ensembles de données plus petits ou différents. 
        ''')       
        
        # Critères de pré-sélectionnement des modèles testés
        st.write("###### - Critères de présélection")
        data = {'Critères': ['Taille du modèle (MB)', 'Accuracy (Top1/Top5)', 'Nombre de paramètres (millions)', 'Temps de calcul CPU/GPU (ms)']}
        
        df = pd.DataFrame(data)
        # Convertir le dataframe en HTML avec les styles CSS
        html_table = df.to_html(index=False, justify='center', classes='styled-table')
        # Afficher le HTML dans Streamlit avec la largeur calculée
        st.markdown(f"<div style='border: 1px solid white; border-radius: 5px; padding: 10px; background-color: #343434; line-height: 1; width: 350px; margin: 0 auto;'>{html_table}</div>", unsafe_allow_html=True)           
        
        
        # Tableau qui résume les modèles choisis pour le Transfer Learning
        st.write("###### - Modèles présélectionnés")
        data = {
            'Modèle': ['InceptionResNet', 'ResNet', 'DenseNet', 'VGG', 'ConvNext', 'EfficientNet'],
            'Versions': ['InceptionResNetV2', 'ResNet121V2', 'DenseNet201', 'VGG16, VGG19', 'ConvNextBase, ConvNextTiny', 'EfficientNetB0, EfficientNetB1, EfficientNetB2, EfficientNetB3, EfficientNetB4, EfficientNetB5, EfficientNetB6']
        }
        df = pd.DataFrame(data)

        # Convertir le dataframe en HTML avec les styles CSS
        html_table = df.to_html(index=False, justify='center', classes='styled-table')

        # Afficher le HTML dans Streamlit avec la largeur calculée
        st.markdown(f"<div style='border: 1px solid white; border-radius: 5px; padding: 10px; background-color: #343434; line-height: 1; width: 350px; margin: 0 auto;'>{html_table}</div>", unsafe_allow_html=True)           

    ### Troisième onglet
    with tab3:
        st.header("Suivi des métriques")
        st.markdown('''
        Dans le domaine du deep learning appliqué à la santé, l'évaluation des modèles joue un rôle crucial pour mesurer leur performance et leur pertinence clinique. 
        Les métriques utilisées fournissent des informations essentielles sur la capacité du modèle à généraliser à de nouvelles données et à fournir des prédictions précises et fiables.
                    ''')
    
        col1, col2 = st.columns(2)

        with col1:
            st.subheader("Précision (accuracy)")
            st.markdown('''
            La précision est l'une des métriques les plus fondamentales en deep learning. 
            Elle mesure la proportion de prédictions correctes parmi toutes les prédictions effectuées par le modèle. 
            Bien qu'elle soit souvent utilisée comme mesure globale de performance, elle peut être trompeuse dans le contexte médical lorsque les classes sont déséquilibrées. 
            Par exemple, dans le diagnostic médical, où les cas positifs sont rares par rapport aux cas négatifs, une haute précision peut être obtenue simplement en prédisant toujours la classe majoritaire (négative), ce qui masquerait l'incapacité du modèle à détecter les cas positifs.
                        ''')

            st.subheader("F1 Score")
            st.markdown('''
            Le score F1 est une mesure qui combine à la fois la précision et la sensibilité en un seul nombre. 
            Il est particulièrement utile lorsque le déséquilibre entre les classes est important, car il prend en compte à la fois les faux positifs et les faux négatifs. 
            Dans le domaine médical, où les conséquences des erreurs de prédiction peuvent être graves, le score F1 est souvent préféré pour évaluer la performance des modèles de diagnostic et de détection des maladies.
                        ''')
        
        with col2:
            st.subheader("Sensibilité et Spécificité")
            st.markdown('''
            La sensibilité (recall) mesure la capacité du modèle à identifier correctement les cas positifs parmi tous les cas réellement positifs. 
            Elle est particulièrement importante dans les applications médicales où la détection précoce des anomalies ou des maladies est cruciale. 
            D'un autre côté, la spécificité mesure la capacité du modèle à identifier correctement les cas négatifs parmi tous les cas réellement négatifs. 
            Ensemble, la sensibilité et la spécificité fournissent une image plus complète de la capacité du modèle à discriminer entre les classes et à minimiser les faux positifs et les faux négatifs.
                        ''')

            st.subheader("Courbe ROC et aire sous la courbe (RAC-AUC)")
            st.markdown('''
            La courbe ROC (Receiver Operating Characteristic) est un graphique qui représente la performance d'un modèle de classification à différents seuils de classification. 
            Elle compare la sensibilité (taux de vrai positif) au taux de faux positif (1 - spécificité) à différents seuils de décision. 
            L'aire sous la courbe (AUC) ROC quantifie la capacité du modèle à discriminer entre les classes et fournit une mesure agrégée de sa performance. 
            Dans le contexte médical, une AUC élevée indique une capacité de diagnostic élevée et une meilleure capacité à séparer les classes.
                        ''')

    with tab4:
            col00, col01, col02 = st.columns([0.4, 0.2,0.4])
            with col01 : 
                Slider = st.select_slider(" ", options = ["Transfer learning" , "Fine Tuning"])

            categorie = {"Transfer learning" :["Modèles testés","InceptionResNetV2","ResNet121V2","DenseNet201","VGG16", "VGG19","ConvNextTiny","ConvNextBase","EfficientNet B4"],
                        "Fine Tuning" : ["EfficientNet", "ResNet", "VGG16_ft" ,"DenseNet"]}

            Choice_cr = st.selectbox("Navigation",
                                    options = categorie[Slider])
            
            csv_path_cr = {"Modèles testés" :r"data\df test model.csv",
                        "InceptionResNetV2" :r"data\df InceptionRes.csv",
                        "ResNet121V2" : r"data\df Res.csv",
                        "DenseNet201": r"data\df densenet.csv",
                        "VGG16" : r"data\df VGG16.csv", 
                        "VGG19" : r"data\df VGG19.csv",
                        "ConvNextTiny" : r"data\df Convtiny.csv",
                        "ConvNextBase" : r"data\df Convbase.csv",
                        "EfficientNet B4" :r"data\df efficient.csv",
                        "EfficientNet" :r"data\df efficientnet finetuned.csv",
                        "ResNet" :r"data\df resnet finetuned.csv",
                        "VGG16_ft" :r"data\df VGG16_finetuned.csv",
                        "DenseNet" :r"data\df densenet_finetuned.csv"}
            
            comm_dico = {"Modèles testés" :"""
                        <div>
                        Voici un récapitulatif des modèles que nous avons testés dans le cadre du transfer learning.<br>
                        Nous avons poursuivi ensuite le fine-tuning avec la répartition suivante.<br>
                        <ul>
                            <li>DenseNet : Alexandre</li>
                            <li>ResNet : Camille</li>
                            <li>VGG16 : Pierre-Jean</li>
                            <li>EfficientNet : Chaouki</li>                         
                        </ul>
                        </div>""",
                         
                        "InceptionResNetV2" :""" 
                        <ul>
                            <li>Le modèle a une capacité variable à distinguer les différentes classes de radiographies. La classe Viral Pneumonia présente d'excellents scores de précision, de rappel et de F1, indiquant une identification quasi parfaite, tandis que la classe Normal a montré des difficultés plus marquées, avec les scores les plus bas pour ces mêmes métriques.</li>
                            <li>Le score F1, qui équilibre la précision et le rappel, suggère que le modèle est plus apte à identifier correctement les classes COVID et Viral Pneumonia,</li>
                            <li><strong>mais qu'il pourrait bénéficier d'un rééquilibrage ou d'un ajustement dans la classification des classes Lung_Opacity et Normal.</strong></li>
                        </ul>""" ,

                        "ResNet121V2" :""" 
                        <ul>
                        <li>Le modèle a une certaine tendance à confondre la classe COVID avec les classes Lung_Opacity et Normal, comme en témoignent les 11 erreurs dans chaque cas. Néanmoins, la classe Viral Pneumonia est interprétée avec une grande précision, indiquant que les caractéristiques distinctives de cette classe sont bien capturées par le modèle.</li>
                        <li>Les métriques par classe montrent que la classe 3 se distingue avec une précision et un rappel exceptionnels proches de 0.98, menant à un score F1 similaire, qui est une mesure robuste de la précision globale. Les classes COVID, Lung_Opacity, et Normal présentent des scores F1 légèrement plus bas, mais toujours respectables, bien que ces classes pourraient bénéficier d'un réajustement du modèle pour améliorer la distinction entre elles.</li>
                        <li><strong>La précision globale du modèle à 0.88 est solide, mais l'objectif serait de viser une amélioration dans la classification fine entre les classes similaires.</strong></li>
                        </ul>""" ,

                        "DenseNet201":"""  
                        <ul>
                            <li>Les erreurs de classification les plus courantes semblent se produire entre les classes Lung_Opacity et Normal, sous-entendant des similarités entre les caractéristiques des radiographies que le modèle confond certainement.</li>
                            <li> Selon le tableau de métriques, le modèle a une excellente précision pour la classe COVID et des scores exceptionnels de rappel et de F1 pour la classe Viral Pneumonia, indiquant une classification presque parfaite pour ces catégories. Les classes Lung_Opacity et Normal ont des scores F1 légèrement inférieurs mais comparables.</li>
                            <li><strong>Tout ceci indique une bonne performance de classification qui reste uniforme entre ces catégories.</strong></li>
                        </ul>""" ,

                        "VGG16" : """ 
                        <ul>
                        <li>Le modèle parvient à très bien classer les radiographies des classes Viral (Viral pneumonia) et COVID. Également, même si les résultats restent bons, le modèle commet plus d'erreurs de classification entre les catégories Normal et Lung (Lung_opacity).</li>
                        <li><strong>Sans ajustement particulier, ce modèle semble déjà prometteur quant à ses capacités à classifier nos radiographies correctement.</strong></li>
                        </ul>""", 

                        "VGG19" : """ 
                        <ul>
                        <li>Les résultats obtenus semblent également très bons et superposables à ceux que nous avons obtenus pour que pour VGG16.</li>
                        <li><strong>Cependant ce modèle étant un peu plus profond, il demande des ressources computationnelles plus importantes sans que cela ne se répercute de façon évidente sur ses performances.</strong></li>
                        </ul> """,

                        "ConvNextTiny" : """ 
                        <ul>
                        <li>Avec ce modèle, il apparaît que la classification est significativement meilleure pour la catégorie Viral (Viral pneumonia) que pour les autres. Ceci donne un score global en deçà de ce que nous avons pu observer sur d’autres modèles dans les mêmes conditions de test.</li>
                        <li>Les courbes d’apprentissage suggèrent que le modèle pourrait bénéficier d’un nombre d'époques supérieur pour continuer à s’améliorer.</li>
                        </ul> """,

                        "ConvNextBase": """
                        <ul>
                        <li>La classe Viral pneumonia reste toujours la mieux détectée, suivie de la classe COVID. Les résultats obtenus ici sont donc comparables à ceux obtenus avec le modèle ConvNeXtTiny.</li>
                        <li>Encore une fois le modèle semble pouvoir bénéficier d’un allongement de la durée d'entraînement. Cependant il est à noter que ce modèle peut se montrer gourmand en termes de ressource computationnelle, <strong>une époque de ConvNeXtBase pouvant prendre entre deux et trois fois plus de temps que le modèle ConvNeXtTiny sans montrer une différence flagrante de performance.</strong></li>
                        </ul>
                        """,
                            "EfficientNet B4": """
                        <ul>
                        <li>La précision du modèle chute à 0.88 sur l’ensemble test. La détection de la classe COVID n'est pas au niveau de ce que l’on espérait avec une précision de 0.91.</li>
                        <li><strong>Globalement, le modèle avec ce paramétrage donne de bons résultats.</strong> Dans la section suivante, nous allons essayer un ajustement plus fin pour avoir de meilleures performances avec ce modèle.</li>
                        </ul>
                        """,
                            "EfficientNet": """
                        <ul>
                        <li><strong>Avec une précision globale de 0.94, c’est le meilleur modèle que nous avons eu pour cette partie concernant la famille de modèles EfficientNet.</strong> De plus, le modèle semble bien plus performant concernant la classe qui nous intéresse ici (classe COVID), avec une reconnaissance des radiographies COVID à 0.98 avec précision.</li>
                        <li>Pour la suite de nos travaux, le meilleur modèle sera adopté et utilisé pour l’interprétabilité et la suite de cette étude.</li>
                        </ul>
                        """,
                            "ResNet": """
                        <ul>
                        <li>Bien que performant, le modèle tend à être freiné dans ses performances par la classe Lung_Opacity, dans laquelle il classe des poumons sains et vice-versa. Quelques poumons sains sont aussi incorrectement classés en Viral Pneumonia.</li>
                        <li><strong>Ce modèle est donc performant, et supprimer la classe Lung_Opacity bénéficierait certainement beaucoup au InceptionResNetV2.</strong></li>
                        </ul>
                        """,
                            "VGG16_ft": """
                        <ul>
                        <li>Le modèle a donc été entraîné avec ces paramètres ce qui nous permet d’améliorer encore l’efficacité du modèle par rapport à ce que nous avions obtenu sans finetuning. Les classes les mieux prédites sont COVID et Viral (Viral pneumonia), suivies par les classes Lung Opacity et Normal.</li>
                        <li>De façon intéressante , toutes nos métriques sont au-dessus de 90% et suite à l'entraînement du modèle avec les meilleurs paramètres nous obtenons une accuracy globale de 95%. <strong>Ce modèle semble donc capable de fournir des résultats plus qu’acceptables tout en ayant un coût computationnel très contenu.</strong></li>
                        </ul>
                        """,
                            "DenseNet": """
                        <ul>
                        <li>Le rapport de classification montre des valeurs élevées pour la précision, le rappel et le F1 Score pour chaque classe ce qui indique que le modèle est particulièrement performant dans la distinction entre les différentes conditions.</li>
                        <li>A noter cependant qu’il performe tout particulièrement dans la distinction de la classe COVID et de la classe Viral Pneumonia mais est un peu moins efficace dans la détection des classes Normal et Lung_Opacity. Pour le COVID, le modèle a très bien performé, avec seulement 3 faux positifs et faux négatifs. Les résultats pour les autres conditions sont également bons, mais on note quelques erreurs, par exemple, 23 cas de Lung_Opacity ont été confondus avec la classe Normal. <strong>Néanmoins, ces erreurs semblent être faibles en comparaison avec le nombre total de prédictions correctes.</strong></li>
                        </ul>
                        """
            }

            CM_dico =  {"Modèles testés" :"",
                        "InceptionResNetV2" :plot_CM_ResNetV2,
                        "ResNet121V2" : plot_CM_ResNet121,
                        "DenseNet201": plot_CM_DenseNet201,
                        "VGG16" : plot_CM_VGG16, 
                        "VGG19" : plot_CM_VGG19,
                        "ConvNextTiny" : plot_CM_ConvnextTiny,
                        "ConvNextBase" : plot_CM_ConvnextBase,
                        "EfficientNet B4" :plot_CM_EfficientNet_B4,
                        "EfficientNet" :plot_CM_ENetB4,
                        "ResNet" :plot_CM_ResNetFT,
                        "VGG16_ft" :plot_CM_VGG16_FT,
                        "DenseNet" :plot_CM_DenseNetFT}

            df = pd.read_csv(csv_path_cr[Choice_cr])
            df= df.fillna("")

            # Convertir le dataframe en HTML avec les styles CSS
            html_table = df.to_html(index=False, justify='center', classes='styled-table')

            # Définir le style CSS pour centrer l'affichage du DataFrame et le fond
            css_style = """
            <style>
                .background-div {
                    max-width: fit-content; /* Largeur adaptée au contenu */
                    margin: 0 auto; /* Centrer horizontalement */
                    padding: 10px;
                    background-color: #343434;
                    border-radius: 5px;
                }
                .inner-div {
                    text-align: center; /* Centrer le contenu */
                }
            </style>
            """

            # Ajouter le style CSS à la balise div
            styled_html_table = f"<div class='background-div'><div class='inner-div'>{html_table}</div></div>"

            col1, col2 = st.columns(2)

            with col1:
                st.markdown(css_style, unsafe_allow_html=True)
                st.markdown(styled_html_table, unsafe_allow_html=True)
                cola ,colb, colc = st.columns([0.2,0.6,0.2])
                with colb:
                    if Choice_cr != "Modèles testés":
                        CM_dico[Choice_cr]()
                    
            
            with col2:
                css_style_text = """
                <style>
                .centered-text {
                    display: flex;
                    justify-content: center;
                    align-items: center;
                    height: 100vh;
                    margin-top: -35%; /* Ajuster la position verticale */
                }
                </style>
                """
                st.markdown(css_style_text, unsafe_allow_html=True)
                st.markdown(f"<div class='centered-text'>{comm_dico[Choice_cr]}</div>", unsafe_allow_html=True)


    ### Cinquième onglet
    with tab5:

        
        best_hp = {"VGG16" : """ 
                   - Dernière couche dense : 1024 neurones
                   - Dropout : 0
                   - Learningrate : 10e-4 """,
                   "DenseNet" : """ 
                    - Dernière couche dense : 256 neurones (Regularisation L2 : 0.01)
                    - Dropout : 0.4,
                    - Learning rate : 10e-4 """}
        

        
        Col1 , Col2 = st.columns(2)

        with Col1:
            st.header("VGG16 métriques")
            plot_precision_curve(history_vgg)
            plot_loss_curve(history_vgg)
            plot_auc(history_vgg)
            plot_f1_score(history_vgg)
            st.markdown(best_hp['VGG16'])
        with Col2:
            st.header("DenseNet métriques")
            plot_precision_curve(history_densenet)
            plot_loss_curve(history_densenet)
            plot_auc(history_densenet)
            plot_f1_score(history_densenet)
            st.markdown(best_hp["DenseNet"])
