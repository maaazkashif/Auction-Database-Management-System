# Auction-Database-Management-System
1. Project Description
The Car Auction Management System is designed to streamline car auctions by managing users, auctions, bids, and car details. This project demonstrates the integration of a normalized database (in BCNF) with a Python-based graphical user interface (GUI). The system provides functionalities for managing records, conducting searches, and ensuring data consistency through relational database design principles.

2. Database Design
  2.1  Schema Design
The database consists of the following tables:
Users Table
Attributes: UserID, Username, Password, Email, Role (Buyer/Seller)
Role ensures users are classified correctly.
Cars Table
Attributes: CarID, Make, Model, Year, Color, Mileage
Ensures unique identification of cars with essential details.
Auction Table
Attributes: AuctionID, CarID, StartTime, EndTime, ReservePrice, CurrentBid, Details, Status, StartingBid
Tracks auctions and links to the Cars table.
Bids Table
Attributes: BidID, AuctionID, UserID, BidAmount, BidTime
Links users with auctions and maintains bidding history.
(Transactions Table Decomposed into two tables resulting in BCNF form)
Transaction Table
Attributes: TransactionID, UserID, AuctionID
Links the TransactionID to UserID and AuctionID
UserPayment Table
Attributes: AuctionID, UserID, PaymentAmount, PaymentDate
Links AuctionID and UserID to PaymentAmount and PaymentDate

2.2 Normalization
All tables in the database are normalized to Boyce-Codd Normal Form (BCNF) by satisfying the following requirements:
Each table has a primary key:
Every table is uniquely identified by a single primary key or a composite primary key, ensuring no duplicate records exist. 
All attributes are fully functionally dependent on the primary key:
For tables with composite keys, each attribute is fully dependent on the entire primary key, eliminating any partial dependencies.
No transitive dependencies exist:
Non-prime attributes (attributes that are not part of any candidate key) depend only on the primary key. No attribute depends on another non-prime attribute, ensuring the elimination of transitive dependencies.
Each functional dependency satisfies BCNF criteria:
For every functional dependency X→YX \rightarrow Y, XX is either a superkey (a set of attributes that uniquely identifies a row) or the dependency does not exist.
No multivalued dependencies:
All attributes are scalar values, ensuring no attribute contains sets, lists, or repeating groups.

Ensuring minimal redundancy:
By achieving BCNF, the schema design reduces duplication and redundancy, optimizing storage and maintaining data integrity.
This strict adherence to BCNF ensures the database schema is robust, consistent, and free from anomalies during updates, deletions, or insertions.
