
# Email Organization System

This project is an automated system that helps in organizing your email inbox by performing the following tasks:
- Classifying emails based on categories such as spam, promotions, and important.
- Automatically deleting spam emails.
- Unsubscribing from spam emails.
- Deleting emails based on predefined conditions, such as date or sender.
  
## Features
1. **Email Classification**: 
   - Uses advanced machine learning algorithms to classify emails into relevant categories.
   - Weighted K-Nearest Neighbors (KNN) or other custom classifiers are used for efficient classification.
   
2. **Spam Detection and Deletion**:
   - Detects spam emails using pre-trained models and predefined rules.
   - Automatically deletes or marks spam emails for removal.

3. **Unsubscribe from Spam**:
   - Identifies subscription emails and provides an option to unsubscribe from unwanted ones.

4. **Automated Email Deletion**:
   - Deletes emails that meet specified criteria such as older than a certain date, specific senders, or keywords.
   
## Technologies Used
- **Python**: Core programming language for developing the project.
- **Machine Learning**: Custom email classifiers for spam detection and email categorization.
- **IMAP**: Email protocol used for fetching emails and performing actions.
- **SMTP**: Protocol for managing email sending functions, such as unsubscribing from spam.

## How It Works
1. **Email Classification**: The system fetches your emails via IMAP and applies a machine learning classifier to determine their category.
2. **Spam Deletion**: Identified spam emails are automatically flagged and deleted based on user preferences.
3. **Unsubscribe**: The system scans for subscription emails and can unsubscribe the user from undesired mailing lists.
4. **Custom Deletions**: Emails older than a set date or those from specific senders can be deleted automatically.

## Future Enhancements
- Add support for more email providers (e.g., Gmail, Outlook).
- Integrate more sophisticated machine learning models for better email classification.
- Provide a user-friendly interface for configuring email management rules.

## License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.

## Contact
For any queries or issues, feel free to contact me at:
- **Email**: saivigneshbadugu143@gmail.com

You can modify or expand on this based on additional features or specifics of your project!
