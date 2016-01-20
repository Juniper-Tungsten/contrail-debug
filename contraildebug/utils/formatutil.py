import logging

log = logging.getLogger('contraildebug.utils.formatter')


def pretty_format(d, prefix='\n', indent=0):
    formatted_dict = prefix
    for key, value in d.iteritems():
        formatted_dict += '\t' * indent + str(key)
        if isinstance(value, dict):
            formatted_dict += '\n'
            formatted_dict = pretty_format(value, formatted_dict,  indent+1)
        else:
            formatted_dict += ':'
            formatted_dict += '\t' + str(value) + '\n'

    return formatted_dict
