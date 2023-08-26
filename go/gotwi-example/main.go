package main

import (
	"context"
	"fmt"
	"os"

	"github.com/michimani/gotwi"
	"github.com/michimani/gotwi/fields"
	"github.com/michimani/gotwi/tweet/managetweet"
	mttypes "github.com/michimani/gotwi/tweet/managetweet/types"
	"github.com/michimani/gotwi/user/userlookup"
	"github.com/michimani/gotwi/user/userlookup/types"
)

func main() {
	in := &gotwi.NewClientInput{
		AuthenticationMethod: gotwi.AuthenMethodOAuth1UserContext,
		OAuthToken:           os.Getenv("TWITTER_ACCESS_TOKEN"),
		OAuthTokenSecret:     os.Getenv("TWITTER_ACCESS_TOKEN_SECRET"),
		Debug:                true,
	}

	c, err := gotwi.NewClient(in)
	if err != nil {
		fmt.Println(err)
		return
	}

	getMe(c)
	// tweet(c)
}

func tweet(c *gotwi.Client) {
	p := &mttypes.CreateInput{
		Text: gotwi.String("This is a test tweet with poll."),
		Poll: &mttypes.CreateInputPoll{
			DurationMinutes: gotwi.Int(5),
			Options: []string{
				"Cyan",
				"Magenta",
				"Yellow",
				"Key plate",
			},
		},
	}

	res, err := managetweet.Create(context.Background(), c, p)
	if err != nil {
		fmt.Println(err.Error())
		return
	}

	fmt.Printf("[%s] %s\n", gotwi.StringValue(res.Data.ID), gotwi.StringValue(res.Data.Text))
}

func getMe(c *gotwi.Client) {
	p := &types.GetMeInput{
		Expansions: fields.ExpansionList{
			fields.ExpansionPinnedTweetID,
		},
		UserFields: fields.UserFieldList{
			fields.UserFieldCreatedAt,
		},
		TweetFields: fields.TweetFieldList{
			fields.TweetFieldCreatedAt,
		},
	}

	u, err := userlookup.GetMe(context.Background(), c, p)
	if err != nil {
		fmt.Println(err)
		return
	}

	fmt.Println("ID:          ", gotwi.StringValue(u.Data.ID))
	fmt.Println("Name:        ", gotwi.StringValue(u.Data.Name))
	fmt.Println("Username:    ", gotwi.StringValue(u.Data.Username))
	fmt.Println("CreatedAt:   ", u.Data.CreatedAt)
	if u.Includes.Tweets != nil {
		for _, t := range u.Includes.Tweets {
			fmt.Println("PinnedTweet: ", gotwi.StringValue(t.Text))
		}
	}
}
