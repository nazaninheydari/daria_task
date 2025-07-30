import pandas as pd
from medical.models import CrossData, LongData

def load_csv_to_mongo(csv_path, mode="cross"):
    df = pd.read_csv(csv_path)
    
    df.dropna(how='all', inplace=True)

    for _, row in df.iterrows():
        doc = CrossData(data=row.to_dict()) if mode == "cross" else LongData(data=row.to_dict())
        doc.save()

    print(f"✅ Loaded {len(df)} rows into {'CrossData' if mode == 'cross' else 'LongData'} collection.")
