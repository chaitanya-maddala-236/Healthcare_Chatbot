from telegram import Update
from telegram.ext import CallbackContext
from sklearn.metrics.pairwise import cosine_similarity
from utils.helper_functions import vectorizer, symptom_vectors, symptoms, get_random_disease, healthcare_data

def handle_messages(update: Update, context: CallbackContext) -> None:
    user_input = update.message.text.lower()

    if user_input == "/exit":
        exit_chat(update, context)
        return

    if context.user_data.get('symptom_input', False):
        context.user_data.clear()
        context.user_data['symptom_input'] = False

        try:
            user_vector = vectorizer.transform([user_input])
            similarity_scores = cosine_similarity(user_vector, symptom_vectors)[0]
            most_similar_index = similarity_scores.argmax()
            most_similar_symptom = symptoms[most_similar_index]

            if similarity_scores[most_similar_index] > 0.9:
                selected_symptom = most_similar_symptom
                disease = get_random_disease(selected_symptom)
                disease_info_response = healthcare_data.get("disease_info", {}).get(disease, {})
                response = (
                    f"Based on the symptom '{selected_symptom}', a possible disease is '{disease}'.\n"
                    f"Generic Medicine(s): {', '.join(disease_info_response.get('generic_medicine', []) or ['No information'])}\n"
                    f"Home Remedy: {', '.join(disease_info_response.get('home_remedy', []) or ['No information'])}"
                )
            else:
                response = "I'm not sure how to respond to that."

            update.message.reply_text(response)

        except Exception as e:
            print(f"An error occurred: {e}")
            update.message.reply_text("Sorry, I encountered an error. Please try again.")

    elif context.user_data.get('disease_info', False):
        context.user_data.clear()
        context.user_data['disease_info'] = False

        try:
            disease = user_input.title()
            disease_info_response = healthcare_data.get("disease_info", {}).get(disease, {})
            if disease_info_response:
                response = (
                    f"Information about the disease '{disease}':\n"
                    f"Symptoms: {', '.join(disease_info_response.get('symptoms', []) or ['No information'])}\n"
                    f"Generic Medicine(s): {', '.join(disease_info_response.get('generic_medicine', []) or ['No information'])}\n"
                    f"Home Remedy: {', '.join(disease_info_response.get('home_remedy', []) or ['No information'])}"
                )
            else:
                response = f"Sorry, I don't have information about the disease '{disease}'."

            update.message.reply_text(response)

        except Exception as e:
            print(f"An error occurred: {e}")
            update.message.reply_text("Sorry, I encountered an error. Please try again.")

    else:
        if user_input == "/symptom":
            input_symptom(update, context)
        elif user_input == "/disease_info":
            context.user_data['disease_info'] = True
            disease_info(update, context)
        else:
            update.message.reply_text("I'm not sure how to respond to that. Type /exit to end the conversation.")
