__author__ = 'Hujie'

import praw

'''
Parameters: submission object, limit of number of comments
Returns: a comment forest which contains all comments in the submission

Due to API delay, it may take a while.
'''
def getComments(submission,limit=100):
    submission.replace_more_comments(limit=limit, threshold=0)
    all_comments = submission.comments
    return all_comments

'''
Prints all comments in comments, for debugging purposes
Parameters: comments object
Returns: none
'''
def showComments(comments):
    flat_comments = praw.helpers.flatten_tree(comments)
    for comment in flat_comments:
        print(comment.body)
'''
Parameters: subreddit string, limit of number of submissions
Returns: list of hottest submissions
'''
def getSubmissions(subreddit_str,limit=100):
    subreddit = r.get_subreddit(subreddit_str)
    return subreddit.get_hot(limit=limit)

'''
Parameters: comment object
Returns: a list with every comment chain (conversation) extending from given comment to a leaf
'''
def getCommentConversations(comment):
    conversations = getCommentConversationsReversed(comment)
    for conversation in conversations:
        conversation.reverse()
    return conversations

'''
Parameters: comment object
Returns: a list with every comment chain (conversation) extending from given comment to a leaf reversed
Reversed because we don't want to prepend to lists in recursive call.
'''
def getCommentConversationsReversed(comment):
    conversations = []
    # base case: single conversation of length 1
    if len(comment.replies) == 0:
        conversations.append([comment])
        return conversations
    # recursion: append myself to all child conversations
    for child in comment.replies:
        childConversations = getCommentConversationsReversed(child)
        for conv in childConversations:
            conv.append(comment)
            conversations.append(conv)
    return conversations

'''
Parameters: submission object
Returns: a list with every conversation (comment chain from root level to leaf comment) in the submission
'''
def getConversations(submission):
    conversations = []
    for comment in getComments(submission):
         conversations = conversations + getCommentConversations(comment)
    return conversations

#  -----------------------------------------------------------------------
#  execution code

user_agent = ("Linux:ConversationalAgentTools:0.0.1 (by /u/0x00FFFF00)")
r = praw.Reddit(user_agent=user_agent)

submissions=getSubmissions("learnpython")
for submission in submissions:
    showComments(getComments(submission))
    '''
    conversations = getConversations(submission)
    for conversation in conversations:
        for comment in conversation:
            print(comment.body)
            print('------------------')
        print('**** end of conversation ****')
    '''
