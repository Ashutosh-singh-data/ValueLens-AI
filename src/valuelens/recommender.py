SEGMENT_RECOMMENDATIONS = {
    'VIP': {
        'action': 'Early access + premium support',
        'description': 'High predicted future value — prioritize retention and white-glove service.',
    },
    'Loyal': {
        'action': 'Loyalty rewards',
        'description': 'Consistent, valuable customers — reinforce the relationship with recognition.',
    },
    'Growth': {
        'action': 'Personalized discounts',
        'description': 'Moderate predicted value — incentivize increased purchase frequency.',
    },
    'At Risk': {
        'action': 'Win-back email campaign',
        'description': 'Low or churn-likely predicted value — attempt reactivation before losing them entirely.',
    },
}


def get_recommendation(segment):
    return SEGMENT_RECOMMENDATIONS.get(segment, {
        'action': 'No action defined',
        'description': 'Unrecognized segment.',
    })


def add_recommendations(df, segment_col='segment'):
    df = df.copy()
    df['recommended_action'] = df[segment_col].map(
        lambda seg: get_recommendation(seg)['action']
    )
    return df