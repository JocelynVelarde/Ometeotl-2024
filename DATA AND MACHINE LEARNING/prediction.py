import pickle

load_model = pickle.load(open("Modelo_Pred_LeafWetness.pkl","rb"))
test_array= [[1.4,1.5,1.6,1.7,1.8,1.9,1.1,1.2],[1.4,1.5,1.6,1.7,1.8,1.9,1.1,1.2]]

result = load_model.predict(test_array)

print(result)

#["SOil 5","Soil 15","Soil 50","Grassland","evaporation"],