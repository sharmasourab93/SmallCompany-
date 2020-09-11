# SmallCompany

A Transport Company's application to accept Fuel expenditure by company's drivers. 

The application's prime over view can be classified into two: 

1. Upload 
2. Retrieve Records/ View Spend Trends 


The Upload section can be classified into two further sub-divisions: 

    1. Upload One Instance of a record at a time 
    2. Upload Bulk/multi-part records through a file. 
    
    
The Retrieval Section has many views: 
    
    1. Spend In a month 
    2. Spend by Fuel Type 
    3. Spend by User/Driver 
    4. Spend Across Drivers & Fuel Types 
    

To access the upload section, I have configured the Landing page on Upload i.e. 
    
    - http://127.0.0.1:8000/upload/ 

Access to Analytics view has been configured to : 
    
    - http://127.0.0.1:8000/trends/
    
All the views are implemented with URL routes as follows: 

*Upload* 

1. SignUp &nbsp;      `/accounts/signup/`   

2. Login &nbsp;       `/accounts/login/ `

3. Logout &nbsp;             `accounts/logout/`  

4. Password Change &nbsp;    `accounts/password-change`

5. Upload Landing View &nbsp; `/upload/`

6. Record Purchase &nbsp; `purchase/`

7. Insert in Bulk Record  &nbsp;   `bulk/`

8. New Fuel Price &nbsp;  `price/`

9. Register New Driver &nbsp; `driverRec/`


*Analytics* 
1. Analytics Landing View &nbsp; `/trends/`

2. Driver View &nbsp; `trends/driver/`
    
    This view Redirects to two more views based on user selection 
        a.  Driver Spend Details - All Records for a Driver
        b.  Driver's Spend By Month - By Month
    
3. Fuel Spend View &nbsp; `fuel/`
    
    This view redirects to two more views based on user selection
        a. Fuel Spend View  - All records for a Fuel
        b. Fuel Spend By Month - By Month
        
4. Total Spend By Month Across All times &nbsp; `spends/`

5. Total Spends Across Fuels & Drivers Specific to Year & Month &nbsp; `choose/`
    
    This view handles two views 
        1. Transactions in a Year, View by Months
        2. Transactions in a Specific Month of a selected Year.
         
6. Visialized View &nbsp; `across/`   
    



### TODOs: 
1. Detail View redirection to Every Month's 
2. Integration with SignUp/Login 
3. Minor UI Corrections
4. Add Test Cases
5. Add Matplotlib
6. Deploying with Gunicon & Nginx
7. Deploying with Docker, K8s


### Resources 
