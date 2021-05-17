# Snek

A slippery Discord bot written in Python 3.6
Uses Discord.py v0.6.0 found at https://github.com/Rapptz/discord.py

## Author:Juan Valencia

## Notes: 
1. Update existing bot to add ISBN support
1. Add a SQLite cache for results from isbn api
1. Add a request queue to help conform to api limits
1. Refactor existing functionality
1. Figure out how to throw this thing into a docker container?
1. Figure out where to host this bad boy

## Resources:
Discord Python API:

https://discordpy.readthedocs.io/en/stable/

Examples:

https://github.com/Rapptz/discord.py/tree/v1.7.2/examples

ISBN Database reference:

https://isbndb.com/apidocs/v2
https://isbndb.com/

## Future architecture
I made this thing back in like 2017.

It was quite a bit ago and I've learned a lot of very useful patterns and have refined my self as an engineer.
I could just remake this thing as I normally do when I iterate over a project, however I wanted
to experiment and add some depth to my github.

I plan on seperating a lot of the core functionality from what is this micro-monolith (lol).
I've already updated it to the latest version of the discord python library.

I have hopes to introduce some new functionality like interactions with apis and DBs as well as 
finding a home for this thing other than my computer.

## Existing Commands

If there is no input listed, the commands don't support any input

### !test
Output: returns length of a message log gathered from a message channel (default function in example)

### !commands
- enhance

Output: returns a list of commands available to user from a file of all commands (not complete)

### !poll
Input: X number of arguments each being a poll value

Output: Starts a poll and pins it to the channel

### !stoppoll
Output: stops the current poll and displays results

### !fprint
- probably remove this one

Input: File Name

Output: takes in the name of a file and prints its contents (not complete)

### !info
- enhace with better stats.

Output: shows diagnostic bot information (Name,Server Size, Channel, Server, Uptime)

### !setplay
- codewise seems to work, but isn't

sets playing to (args)

### !gn
- enhance, doesnt do much

sends message 'Good Night Everybody!'

### !remindme
- implement better

takes int x minutes and string and notifies user in x amount of minutes of string

### !disconnect
- add permission checking

disconnect command (note terminates all bot processes)
  
## Future Commands

### !book
Input: ISBN-10, ISBN-13, or name of book

Output: If it's an ISBN, it'll output book details, if its book name, it will try to find the ISBN and details


### !AddBookToMyList
- Internally this will require some db work to manage users with their given list
- Consider adding this to stats
- Consider adding number of cached books to stats

Input: `ISBN-10 | ISBN-13`, name of list

Output: Will confirm the name of the list, number of books in list, and the recent added book

### !RandomBook
Output: Returns a random book from a specific subject
