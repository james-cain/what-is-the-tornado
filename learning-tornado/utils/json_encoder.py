import json  
import datetime  
import dateutil.parser  
import decimal

class CustomJsonEncoder(json.JSONEncoder):  
    def default(self, obj):  
        if isinstance(obj, (datetime.datetime,)):  
            return {"val": obj.isoformat(), "_spec_type": "datetime"}  
        elif isinstance(obj, (decimal.Decimal,)):  
            return {"val": str(obj), "_spec_type": "decimal"}  
        else:  
            return super().default(obj
