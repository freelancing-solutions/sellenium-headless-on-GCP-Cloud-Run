

# endpoints

    - api: /browse/login
    - description:  call to login either with username or password or without    
    
    - api: /browse/parse-stock
    - description: call to parse stock
    - required variables: "symbol"
    - optional url, from_date, to_date
    
    - api: /browse/parse-broker
    - description: call to parse broker
    - required variables: "broker_code"
    - optional url, from_date, to_date
     