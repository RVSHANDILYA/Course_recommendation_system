import sqlite3
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity

def get_user_course_data():
    conn = sqlite3.connect('course_recommendation.db')
    
    query = '''
    SELECT users.id AS user_id, users.name, courses.id AS course_id, courses.title
    FROM user_courses
    JOIN users ON user_courses.user_id = users.id
    JOIN courses ON user_courses.course_id = courses.id
    '''
    
    user_course_data = pd.read_sql(query, conn)
    conn.close()
    
    return user_course_data

def get_recommendations(user_id):
    user_course_data = get_user_course_data()
    
    user_course_matrix = user_course_data.pivot_table(index='user_id', columns='course_id', aggfunc='size', fill_value=0)

    cosine_sim = cosine_similarity(user_course_matrix)
    
    sim_df = pd.DataFrame(cosine_sim, index=user_course_matrix.index, columns=user_course_matrix.index)

    similar_users = sim_df[user_id].sort_values(ascending=False).index.tolist()

    recommended_courses_ids = set()
    
    current_courses_ids = set(user_course_data[user_course_data['user_id'] == user_id]['course_id'].tolist())

    for similar_user in similar_users:
        if similar_user != user_id:
            courses_taken_ids = user_course_data[user_course_data['user_id'] == similar_user]['course_id'].tolist()
            recommended_courses_ids.update(courses_taken_ids)

    # Exclude courses already taken by the user
    recommended_courses_ids = list(recommended_courses_ids - current_courses_ids)

    # Fetch course titles based on recommended course IDs
    recommended_courses_titles = get_course_titles(recommended_courses_ids)

    return recommended_courses_titles

def get_course_titles(course_ids):
    conn = sqlite3.connect('course_recommendation.db')
    cursor = conn.cursor()

    # Fetch titles for the given course IDs
    cursor.execute('SELECT title FROM courses WHERE id IN ({})'.format(','.join('?' * len(course_ids))), course_ids)
    
    titles = [row[0] for row in cursor.fetchall()]
    
    conn.close()
    
    return titles