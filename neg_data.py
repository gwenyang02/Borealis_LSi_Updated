# function to create "negative datafile" from CSV fire location data
# reads CSV file and creates new CSV file with dates subtracted by 3 months

def create_neg(csv_file):
    import pandas as pd
    df = pd.read_csv(csv_file)

    # create empty lists to store duplicate coordinates and subtracted dates
    duplicate_coordinates = []
    subtracted_dates = []

    # group data by lat long and date and count number of occurrences
    count_coord_df = df.groupby(['latitude', 'longitude', 'acq_date']).size().reset_index(name='count')
    print('\nCount by coordinate and date:')
    print(count_coord_df)

    # find coordinates that appear more than once, and make new dataframe
    for i, row in count_coord_df.iterrows():
        if row['count'] > 1:
            lat = row['latitude']
            lon = row['longitude']
            temp_df = df[(df['latitude'] == lat) & (df['longitude'] == lon)]
            acq_dates = list(pd.to_datetime(temp_df['acq_date']) - pd.DateOffset(months=3))
            duplicate_coordinates.extend([(lat, lon)] * len(acq_dates))
            subtracted_dates.extend(acq_dates)

    # create a new dataframe from the lists of coordinates and dates
    neg_df = pd.DataFrame({
        'latitude': [coord[0] for coord in duplicate_coordinates],
        'longitude': [coord[1] for coord in duplicate_coordinates],
        'acq_date': subtracted_dates,
    })
    # save the new dataframe to a CSV file
    return neg_df.to_csv('neg_data.csv', index=False)









