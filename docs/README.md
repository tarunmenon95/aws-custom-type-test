# rnd::s3cleanup::test

An example resource schema demonstrating some basic constructs and validation rules.

## Syntax

To declare this entity in your AWS CloudFormation template, use the following syntax:

### JSON

<pre>
{
    "Type" : "rnd::s3cleanup::test",
    "Properties" : {
        "<a href="#functionname" title="FunctionName">FunctionName</a>" : <i>String</i>,
        "<a href="#runtime" title="Runtime">Runtime</a>" : <i>String</i>,
    }
}
</pre>

### YAML

<pre>
Type: rnd::s3cleanup::test
Properties:
    <a href="#functionname" title="FunctionName">FunctionName</a>: <i>String</i>
    <a href="#runtime" title="Runtime">Runtime</a>: <i>String</i>
</pre>

## Properties

#### FunctionName

name to call the function

_Required_: Yes

_Type_: String

_Minimum Length_: <code>1</code>

_Maximum Length_: <code>219</code>

_Update requires_: [No interruption](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/using-cfn-updating-stacks-update-behaviors.html#update-no-interrupt)

#### Runtime

The python runtime for the lambda eg: 'python3.9

_Required_: Yes

_Type_: String

_Update requires_: [No interruption](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/using-cfn-updating-stacks-update-behaviors.html#update-no-interrupt)

## Return Values

### Ref

When you pass the logical ID of this resource to the intrinsic `Ref` function, Ref returns the FunctionArn.

### Fn::GetAtt

The `Fn::GetAtt` intrinsic function returns a value for a specified attribute of this type. The following are the available attributes and sample return values.

For more information about using the `Fn::GetAtt` intrinsic function, see [Fn::GetAtt](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/intrinsic-function-reference-getatt.html).

#### FunctionArn

Function ARN

