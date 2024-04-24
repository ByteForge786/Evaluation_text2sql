# Function to execute queries and check if results are similar
def check_results_similarity(predicted_queries, true_queries):
    similarity_list = []

    for predicted_query, true_query in zip(predicted_queries, true_queries):
        # Extract column names from both queries
        predicted_columns = [col.strip() for col in predicted_query.split('SELECT')[1].split('FROM')[0].split(',')]
        true_columns = [col.strip() for col in true_query.split('SELECT')[1].split('FROM')[0].split(',')]

        # If one query uses '*' and the other uses specific column names
        if '*' in predicted_columns or '*' in true_columns:
            # Get common column names
            common_columns = set(predicted_columns) & set(true_columns)
            # If there are common columns, compare only those
            if common_columns:
                common_columns_str = ', '.join(common_columns)
                predicted_query = predicted_query.replace('*', common_columns_str)
                true_query = true_query.replace('*', common_columns_str)

        # Execute the SQL queries on the respective DataFrames
        predicted_result_df = pd.read_sql_query(predicted_query, conn)
        true_result_df = pd.read_sql_query(true_query, conn)

        # Check if results are similar for each pair of queries
        similarity = 'Yes' if predicted_result_df.equals(true_result_df) else 'No'
        similarity_list.append(similarity)

        print(f"Results for Predicted Query:\n{predicted_query}\nand\nTrue Query:\n{true_query}\nare {similarity}")

    return similarity_list
