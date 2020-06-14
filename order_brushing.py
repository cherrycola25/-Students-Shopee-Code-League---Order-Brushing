import numpy as np
import pandas as pd

df = pd.read_csv('order_brush_order.csv', parse_dates=[3])
#create list of unique shop ids
shopids=df.shopid.unique()

#initialise order brushing dataframe will all userids as 0
order_brushing=pd.DataFrame({'shopid':shopids,'userid':0})

for shop in shopids:
    #look at the data for an indiviudal shop
    indivshopdata=df[(df.shopid==shop)]
    #sort by datetime
    indivshopdata.event_time.sort_values()
    #get a list of individual times
    times=indivshopdata.event_time.unique()
    #look at a given individual time and collate data for a 1 hr interval after that time
    for start_time in times:
        #determine 1 hour after that specific time
        end_time = start_time + pd.Timedelta(hours=1)
        #get data for 1 hour interval
        hour_interval = indivshopdata[(indivshopdata['event_time'] >= start_time) & (indivshopdata['event_time'] <= end_time)]
        #get number of orders in that 1hr time period
        n_orders=hour_interval.orderid.nunique()
        #get number of unique users in that 1hr
        n_users=hour_interval.userid.nunique()
        #find conc rate
        conc_rate=n_orders/n_users
        #find most frequent user/s
        most_freq_user=hour_interval.userid.mode()
        #update order brushing dataframe with frequent user/s if order brushing occurs
        if conc_rate>=3:
            #remove current shopid entry that has 0 for userid
            order_brushing=order_brushing[order_brushing['shopid']!=shop]
            #replace with shopid entry and userid of frequent user/s
            for user in most_freq_user:
                order_brushing = order_brushing.append({'shopid': shop, 'userid':user}, ignore_index=True)



#remove duplicate entries
order_brushing.drop_duplicates(keep=False,inplace=True)
print(order_brushing)
order_brushing.to_csv('order_brushing.csv', index = False)
