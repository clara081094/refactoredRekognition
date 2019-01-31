import datetime
from datetime import timedelta
from dataManage import DataManage
from redshiftManage import RedshiftManage

if __name__ == '__main__':


        dayCompare = (datetime.datetime.now()-timedelta(hours=48)).date()
        print("dayCompare: ",dayCompare)
        rows = DataManage().obtain_rows_date(dayCompare)

        if len(rows) == 0 :
            print("No registers for RedShift")
        else:
            #faceId,dateFace,place,grop
            for record in rows :
                RedshiftManage().add_register(
                    record['faceId'],
                    datetime.datetime.strptime(record['fecha'],"%Y-%m-%d %H:%M:%S.%f")+timedelta(hours=5),
                    record['camara'],
                    record['caracteristicas']

                )


