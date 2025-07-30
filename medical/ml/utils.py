import pandas as pd
from medical.models import CrossData, LongData

def get_combined_data():
    cross_docs = CrossData.objects()
    long_docs = LongData.objects()

    df_cross = pd.DataFrame([doc.data for doc in cross_docs])
    df_long = pd.DataFrame([doc.data for doc in long_docs])

    combined_df = pd.concat([df_cross, df_long], ignore_index=True)

    return combined_df
