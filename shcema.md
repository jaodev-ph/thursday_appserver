tenant
    - name | string
    - contact_number | string
    - email_address | string
    - address | string
    - logo | string
    - geolocation | list
    - bot_id | ObjectId
    - business_type | list

admin
    - username
    - password

user
    - tenant_id | ObjectId
    - name | string
    - contact_number | string
    - email_address | string
    - address | string
    - acl_profile_id | ObjectId

bot
    - tenand_id
    - name
    - model
    
conversation
    - tenant_id | ObjectId
    - bot_id | ObjectId
    - channel | str
    - customer | ObjectId
    - status | string
    - token_usage | Dict

customer
    - tenant_id | ObjectId
    - name | string
    - avatart | string
    - contact_number | string
    - email_address | string
    - address | string
    - channel_type | int # CHANNEL_TYPES
    - active | bool

message
    - tenant_id | ObjectId
    - conversation_id | ObjectId
    - customer_id | ObjectId
    - status | int
    - content | string
    - sender_type | int # SENDER_TYPES
    - token_usage | Dict
    - active | bool

billing
    - tenant_id | ObjectId
    - plan | string
    - start_date | datetime
    - end_date | datetime
    - status | int # BILLING_STATUS