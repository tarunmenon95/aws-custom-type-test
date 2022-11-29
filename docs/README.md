# rnd::s3cleanup::test

An example resource schema demonstrating some basic constructs and validation rules.

## Syntax

To declare this entity in your AWS CloudFormation template, use the following syntax:

### JSON

<pre>
{
    "Type" : "rnd::s3cleanup::test",
    "Properties" : {
        "<a href="#name" title="Name">Name</a>" : <i>String</i>,
        "<a href="#runtime" title="Runtime">Runtime</a>" : <i>String</i>
    }
}
</pre>

### YAML

<pre>
Type: rnd::s3cleanup::test
Properties:
    <a href="#name" title="Name">Name</a>: <i>String</i>
    <a href="#runtime" title="Runtime">Runtime</a>: <i>String</i>
</pre>

## Properties

#### Name

A name associated with the s3 bucket.

_Required_: Yes

_Type_: String

_Minimum Length_: <code>1</code>

_Maximum Length_: <code>219</code>

_Update requires_: [Replacement](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/using-cfn-updating-stacks-update-behaviors.html#update-replacement)

#### Runtime

The python runtime eg: 'python3.9

_Required_: Yes

_Type_: String

_Update requires_: [No interruption](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/using-cfn-updating-stacks-update-behaviors.html#update-no-interrupt)

## Return Values

### Ref

When you pass the logical ID of this resource to the intrinsic `Ref` function, Ref returns the Name.
