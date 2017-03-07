
'''
dag = DAG('feature_extraction', default_args=default_args)


op_kwargs = {
    'segmentation_server': segmentation_server,
    'classification_server': classification_server
}

t1 = PythonOperator(
    task_id='feature_extraction',
    provide_context=True,
    python_callable=feature_extraction,
    op_kwargs=op_kwargs,
    dag=dag)

t2 = PythonOperator(
    task_id='feature_extraction',
    provide_context=True,
    python_callable=feature_extraction,
    op_kwargs=op_kwargs,
    dag=dag)
'''

