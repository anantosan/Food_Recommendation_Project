# Food Recommendation Project

![MasakuLogo](/screenshot/Masaku_Logo.png)

This Project called **Masaku** (Masak Sisa Bahan di Kulkas) is a Flask App that will recommend you what to cook based on what is left on your fridge using Content-Based Filtering.

The dataset used for the recommendation is from [Kaggle](https://www.kaggle.com/canggih/indonesian-food-recipes) Indonesian Food Recipes by scraping the data from [Cookpad](https://www.cookpad.com). You can easily choose what's your main dish and input another supporting ingredients that you have. After that, the app will give you five recommendation food to cook.

There are six feature from this app that you can access.

1. Home Page

    This is the first page when you open it. In this page, you should Log in first to continue to Recommendation page.

    ![Home](/screenshot/home.png)

    If you directly click to the recomendation bar or type an unregistered account, you will be directed to error page.

    ![error](/screenshot/error_loginfirst.png)

    Or if you type the wrong password, you will also directed to error page.

    ![errorpwd](/screenshot/error_wrongpwd.png)

2. Sign Up Page

    If you don't have any account registered in database, you can sign up in this page.

    ![signup](/screenshot/signup.png)

    But if you sign up with username that already exist, you will be directed to error page.

    ![error](/screenshot/error_userexist.png)

    After you successfully sign in or sign up, there will be current user appear in the right top of navbar. You can also sign out from it.

3. Recommendation Page

     In this page, you can choose what **main dish** do you want to cook, type **supporting ingredients** left on your fridge, and click the button to know what are the recommendation for you.

    ![recommendation](/screenshot/recommendation.png)

4. Result Page

    These are your five recomendation food to cook based on what's left on your fridge. You can also find out its full receipt by clicking it.

    ![Result](/screenshot/result.png)

5. Full Receipt Page
    
    This is the full receipt of the food that you choose. 

    ![FullReceipt](/screenshot/full_receipt.png)

There are also two supporting page that you can access with out login.

1. About Page

    ![About](/screenshot/About.png)

2. Visualization Page

    ![Visual](/screenshot/visualize.png)

If you want to try this, You could clone this Github and try to run _app. py_

Let's Cook!


#
#### Author : Mochamad Ihsan Ananto
#### Reach me out : _anantosan97@gmail.com_

[GitHub](https://github.com/anantosan)
|
[LinkedIn](https://www.linkedin.com/in/mochamad-ihsan-ananto-4a70b8123/)