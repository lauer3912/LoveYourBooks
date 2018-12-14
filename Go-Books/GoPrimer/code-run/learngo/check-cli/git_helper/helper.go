package git_helper

import "fmt"

type GitHelper struct {
	Version string
	docs    []string
}

func (helper *GitHelper) String() string {
	return fmt.Sprintf("implement me")
}

func (helper *GitHelper) GetDoc() (doc string) {
	helper.Version = "0.1.0"
	doc = fmt.Sprintf("%s Ver%s", "GitHelper", helper.Version)

	for _, one_content := range helper.docs {
		doc = doc + one_content
	}

	return doc
}