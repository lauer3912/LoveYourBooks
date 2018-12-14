package main

import (
	"fmt"
	"golang.org/x/tools/container/intsets"
	"./git_helper"
)


func testSparse() {
	s := intsets.Sparse{}

	s.Insert(1)
	s.Insert(10000)
	s.Insert(29993)

	fmt.Println(s)
}

func testGitHelper() {
	helper := git_helper.GitHelper{}
	fmt.Println(helper)

	docs := helper.GetDoc()
	fmt.Println(docs)
}


func main() {
	fmt.Println("Hello! Check-CLI")

	testSparse()

	testGitHelper()

}
