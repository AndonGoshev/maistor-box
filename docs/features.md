## Features 🧑‍💻

- ### 🪪 Accounts

	- #### 👤 Regular users have option for quick account setup with only few fields.

	- #### 👷 Contractor users have extended registration process with multiple layers of account maintainability.
		- Extended form for registration with personal and public data fields
		- Feature for managing and displaying projects efficiently
		- User-friendly interface for editing/updating contractor's profile and its projects

	- #### ⚙️ Easily maintainable accounts generic features
		- Welcoming email for every registration
		- Change password
		- Forgotten password
		- Deleting account

- ### 🔍 SearchBoard

	- ### 📜 Search forms
		- Clean and user-friendly search forms. Main one on the home-page (landing page) and one on the top of the
		  Search board.

	- ### 🔍 Search board
		- Clean and simple search board displaying list of contractor based on chosen specializations/regions criteria.
		- Paginator dividing the results on pages by 12 contractors.

- ### Common

	- ### 🏠 Landing page
		- Beautifully designed home page with all the features and info needed, for a user to know what this application
		  is about, when 'lands' on it.
		- Simple yet thoughtfully-styled UI and intuitive UX design.

	- ### 👷 Contractor Public Profile Model
		- Separated from the main contractor account - this is the public profile for every contractor.
		- Every time when a contractor user register ,automatically this public profile is created.
		- Whatever public data is changed in the main account model - it's updated in the public profile too ,but this
		  public model is strictly used only for public data displaying and separates itself from the private account
		  data.
		- Field Slug: A specifically created field designed to handle the logic for the business card option for
		  contractors. With this approach, the URL for a public profile will be formatted
		  as www.maistorbox.com/john-doe.
		  This feature allows contractors to have business cards with clean, human-readable URL links for their online
		  presence. While this is a planned future functionality, it is being implemented with a solid foundation.

	- ### 📝 Client Feedback Model
		- Completely related only to the public model.
		- Gives straightforward option for every registered user in the application to leave a feedback.
		- Feedback options - rating stars(mandatory) and comment(optional)
		- When submitted the feedback is up for approval. An authorised admin (group = Client feedback redactor) will
		  review the feedback and decides if it appropriate.

- ### 🏢 Company

	- ### 🗂️ Company model
		- Model with only one instance permitted, dedicated for saving all the **MaistorBox Company** ralated data.
		- When company data is needed ,easily can be retrieved from this model.

	- ### 📨 Message model
		- Model dedicated for receiving user messages in the contacts page.
		- When user sends a message it's saved in the ✉️database as well it's received as 📧email in the maistorbox
		  inbox.